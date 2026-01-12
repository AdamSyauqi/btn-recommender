from __future__ import annotations

import hashlib
import json
import random
from collections import deque
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Dict, Tuple, Optional

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from recommender.models import RecommendationEvent
from recommender.tree_konven import TREE


SESSION_KEY_PREFIX = "mgmt_generated"


def _merge_meta(current: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(current or {})
    for k, v in (incoming or {}).items():
        if v is None:
            continue
        if isinstance(v, str) and v.strip() == "":
            continue
        merged[k] = v
    return merged


def _stable_hash(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class State:
    node_id: str
    answers: Dict[str, str]
    meta: Dict[str, Any]
    depth: int


class Command(BaseCommand):
    help = "Generate RecommendationEvent rows from TREE (exhaustive or random)."

    def add_arguments(self, parser):
        parser.add_argument("--start", default="q1", help="Start node id (default: q1)")
        parser.add_argument("--max-depth", type=int, default=50, help="Max traversal depth (default: 50)")

        # Exhaustive mode knobs
        parser.add_argument("--limit", type=int, default=0, help="Stop after creating N events (0=no limit)")
        parser.add_argument("--dedupe", action="store_true", help="Skip inserting if identical generated event already exists")

        # Random mode knobs
        parser.add_argument("--random", type=int, default=0, help="Generate N random runs (0=disabled)")
        parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
        parser.add_argument("--uniform", action="store_true", help="Choose choices uniformly (default is uniform anyway; reserved for future weighting)")
        parser.add_argument("--start-days-ago", type=int, default=0,
                            help="If >0, spread created_at randomly over the last N days (requires created_at editable or post-update)")

        # Common knobs
        parser.add_argument("--dry-run", action="store_true", help="Do not write to DB; just report")
        parser.add_argument("--delete-generated", action="store_true",
                            help=f"Delete events whose session_key starts with '{SESSION_KEY_PREFIX}' before generating")

    def handle(self, *args, **opts):
        start = opts["start"]
        max_depth = opts["max_depth"]
        limit = opts["limit"]
        dedupe = opts["dedupe"]

        random_n = opts["random"]
        seed = opts["seed"]
        dry_run = opts["dry_run"]
        delete_generated = opts["delete_generated"]
        start_days_ago = opts["start_days_ago"]

        if start not in TREE:
            self.stderr.write(self.style.ERROR(f"Start node '{start}' not found in TREE"))
            return

        if seed is not None:
            random.seed(seed)

        if delete_generated and not dry_run:
            deleted, _ = RecommendationEvent.objects.filter(session_key__startswith=SESSION_KEY_PREFIX).delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} previously generated events."))

        # Preload existing hashes for dedupe (only for exhaustive mode; for random mode, dedupe usually not desired)
        existing_hashes = set()
        if dedupe and not dry_run and random_n == 0:
            qs = RecommendationEvent.objects.filter(session_key__startswith=SESSION_KEY_PREFIX).only("answers")
            for ev in qs.iterator(chunk_size=2000):
                existing_hashes.add(_stable_hash(ev.answers or {}))

        created_count = 0
        leaf_hits = 0
        missing_nodes = 0
        dead_ends = 0
        skipped_dedupe = 0

        @transaction.atomic
        def _create_event(leaf_node_id: str, node: Dict[str, Any], answers: Dict[str, str], meta: Dict[str, Any]) -> Optional[int]:
            nonlocal created_count, skipped_dedupe

            answers_hash = _stable_hash(answers)

            if dedupe and random_n == 0:
                if answers_hash in existing_hashes:
                    skipped_dedupe += 1
                    return None
                existing_hashes.add(answers_hash)

            if dry_run:
                created_count += 1
                return None

            ev = RecommendationEvent.objects.create(
                session_key=f"{SESSION_KEY_PREFIX}:{leaf_node_id}:{answers_hash[:12]}:{created_count+1}",
                answers=answers,
                recommended_products=node.get("products", []),
                product_links=node.get("links", []),
                segment=meta.get("segment", ""),
                customer_type=meta.get("customer_type", ""),
                goal=meta.get("goal", ""),
            )

            # Optional: spread timestamps (if you want charts to look real)
            # This only works if created_at is auto_now_add and still writable via update().
            if start_days_ago and start_days_ago > 0:
                now = timezone.now()
                delta_seconds = random.randint(0, start_days_ago * 24 * 3600)
                fake_time = now - timedelta(seconds=delta_seconds)
                RecommendationEvent.objects.filter(id=ev.id).update(created_at=fake_time)

            created_count += 1
            return ev.id

        # ------------------------
        # RANDOM MODE
        # ------------------------
        if random_n and random_n > 0:
            # In random mode, we intentionally allow duplicates (like real users).
            # So we do NOT dedupe by default (even if --dedupe was passed).
            if dedupe:
                self.stdout.write(self.style.WARNING("Note: --dedupe is ignored in --random mode (duplicates are expected)."))

            for _ in range(random_n):
                leaf_id, leaf_node, answers, meta = self._simulate_one_run(start, max_depth)
                if leaf_node is None:
                    dead_ends += 1
                    continue

                leaf_hits += 1
                _create_event(leaf_id, leaf_node, answers, meta)

                if limit and created_count >= limit:
                    break

            self._report(
                mode=f"random ({random_n})",
                created=created_count,
                leaf_hits=leaf_hits,
                dead_ends=dead_ends,
                missing_nodes=missing_nodes,
                skipped_dedupe=skipped_dedupe,
                dry_run=dry_run,
                seed=seed,
            )
            return

        # ------------------------
        # EXHAUSTIVE MODE
        # ------------------------
        queue = deque([State(node_id=start, answers={}, meta={}, depth=0)])
        visited = set()  # (node_id, answers_hash) loop protection

        while queue:
            state = queue.popleft()
            if state.depth > max_depth:
                continue

            node = TREE.get(state.node_id)
            if not node:
                missing_nodes += 1
                continue

            meta = _merge_meta(state.meta, node.get("meta", {}))
            key = (state.node_id, _stable_hash(state.answers))
            if key in visited:
                continue
            visited.add(key)

            if node.get("leaf") is True:
                leaf_hits += 1
                _create_event(state.node_id, node, state.answers, meta)
                if limit and created_count >= limit:
                    break
                continue

            choices = node.get("choices", {})
            if not isinstance(choices, dict) or not choices:
                dead_ends += 1
                continue

            for choice_key, info in choices.items():
                nxt = info.get("next")
                if not nxt:
                    continue
                new_answers = dict(state.answers)
                new_answers[state.node_id] = choice_key
                queue.append(State(node_id=nxt, answers=new_answers, meta=meta, depth=state.depth + 1))

        self._report(
            mode="exhaustive",
            created=created_count,
            leaf_hits=leaf_hits,
            dead_ends=dead_ends,
            missing_nodes=missing_nodes,
            skipped_dedupe=skipped_dedupe,
            dry_run=dry_run,
            seed=seed,
        )

    def _simulate_one_run(self, start: str, max_depth: int) -> Tuple[str, Optional[Dict[str, Any]], Dict[str, str], Dict[str, Any]]:
        """
        Walk from start -> randomly pick a choice each step until leaf or dead-end.
        Returns: (leaf_id, leaf_node_or_None, answers, meta)
        """
        node_id = start
        answers: Dict[str, str] = {}
        meta: Dict[str, Any] = {}
        depth = 0

        while depth <= max_depth:
            node = TREE.get(node_id)
            if not node:
                return node_id, None, answers, meta

            meta = _merge_meta(meta, node.get("meta", {}))

            if node.get("leaf") is True:
                return node_id, node, answers, meta

            choices = node.get("choices", {})
            if not isinstance(choices, dict) or not choices:
                return node_id, None, answers, meta

            choice_key = random.choice(list(choices.keys()))
            answers[node_id] = choice_key
            node_id = choices[choice_key].get("next")
            if not node_id:
                return "", None, answers, meta

            depth += 1

        return node_id, None, answers, meta

    def _report(
        self,
        mode: str,
        created: int,
        leaf_hits: int,
        dead_ends: int,
        missing_nodes: int,
        skipped_dedupe: int,
        dry_run: bool,
        seed: Optional[int],
    ) -> None:
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Generation finished ({mode})."))
        self.stdout.write(f"Events created: {created}" + (" (dry-run; not saved)" if dry_run else ""))
        self.stdout.write(f"Leaf hits: {leaf_hits}")
        if skipped_dedupe:
            self.stdout.write(f"Skipped due to dedupe: {skipped_dedupe}")
        if dead_ends:
            self.stdout.write(self.style.WARNING(f"Dead ends encountered: {dead_ends} (nodes without choices)"))
        if missing_nodes:
            self.stdout.write(self.style.WARNING(f"Missing nodes referenced: {missing_nodes}"))
        if seed is not None:
            self.stdout.write(f"Seed: {seed}")
