from __future__ import annotations

import base64
import io

from typing import Any, Dict

from collections import Counter

import matplotlib
matplotlib.use("Agg")  # server-safe backend
import matplotlib.pyplot as plt

from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from .models import RecommendationEvent
from .tree_konven import TREE

SESSION_ANSWERS_KEY = "btn_answers"          # Dict[node_id -> choice_key]
SESSION_NODE_KEY = "btn_node"               # current node id
SESSION_META_KEY = "btn_meta"               # accumulated meta: segment/customer_type/goal/etc
SESSION_LAST_EVENT_ID = "btn_last_event_id" # prevent duplicate logging on refresh

def _is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def admin_required(view_func):
    """
    - If not logged in: redirect to recommender:login
    - If logged in but not admin: 403
    """
    @login_required(login_url="recommender:login")
    @user_passes_test(_is_admin, login_url="recommender:login")
    def _wrapped(request, *args, **kwargs):
        # user_passes_test redirects non-admins to login by default;
        # we prefer 403 if they ARE logged in but not admin.
        if request.user.is_authenticated and not _is_admin(request.user):
            return HttpResponseForbidden("Forbidden")
        return view_func(request, *args, **kwargs)
    return _wrapped


def login_view(request):
    """
    Simple admin login page.
    Redirects to ?next=... if provided; otherwise goes to analytics.
    """
    next_url = request.GET.get("next") or request.POST.get("next") or reverse("recommender:analytics")

    # If already logged in as admin, go straight to analytics
    if request.user.is_authenticated and _is_admin(request.user):
        return redirect(next_url)

    error = ""
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""

        user = authenticate(request, username=username, password=password)
        if user is None:
            error = "Invalid username or password."
        else:
            if not _is_admin(user):
                error = "This account is not allowed to access analytics."
            else:
                dj_login(request, user)
                return redirect(next_url)

    return render(request, "recommender/login.html", {
        "error": error,
        "next": next_url,
    })


def logout_view(request):
    dj_logout(request)
    return redirect("recommender:login")

def _ensure_session(request) -> None:
    if not request.session.session_key:
        request.session.create()

def _reset_flow(request) -> None:
    request.session[SESSION_ANSWERS_KEY] = {}
    request.session[SESSION_NODE_KEY] = "q1"
    request.session[SESSION_META_KEY] = {}
    request.session.pop(SESSION_LAST_EVENT_ID, None)
    request.session.modified = True

def _merge_meta(current: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge meta dicts. Later nodes can override earlier ones (e.g. goal changes by branch).
    """
    merged = dict(current or {})
    for k, v in (incoming or {}).items():
        if v is None:
            continue
        if isinstance(v, str) and v.strip() == "":
            continue
        merged[k] = v
    return merged

def start_questionnaire(request):
    _ensure_session(request)
    _reset_flow(request)
    return redirect("recommender:question")

def question(request):
    """
    One-question-per-page wizard.
    - GET shows current question node
    - POST records answer and advances
    - If node becomes leaf -> create RecommendationEvent and redirect to result page
    """
    _ensure_session(request)

    node_id = request.session.get(SESSION_NODE_KEY, "q1")
    node = TREE.get(node_id)
    if not node:
        # unknown node => restart cleanly
        _reset_flow(request)
        return redirect("recommender:question")

    # Accumulate meta from current node (some nodes define goal/customer_type/etc)
    meta = request.session.get(SESSION_META_KEY, {})
    meta = _merge_meta(meta, node.get("meta", {}))
    request.session[SESSION_META_KEY] = meta
    request.session.modified = True

    # If current node is leaf, log recommendation and go to result
    if node.get("leaf") is True:
        return _handle_leaf(request, node_id, node)

        # For non-leaf nodes, show question and options
    if request.method == "POST":
        action = request.POST.get("action", "next")

        # --- RESET / START OVER ---
        if action == "reset":
            _reset_flow(request)
            return redirect("recommender:question")

        # --- NEXT ---
        choice = request.POST.get("choice")
        choices_dict = node.get("choices", {})

        if not choice or choice not in choices_dict:
            # Re-render with an error
            choices = [(k, v["label"]) for k, v in choices_dict.items()]
            return render(
                request,
                "recommender/question.html",
                {
                    "node_id": node_id,
                    "question": node["text"],
                    "choices": choices,
                    "error": "Please select one option.",
                },
            )

        # Store answer: key by node_id (robust for deep trees)
        answers = request.session.get(SESSION_ANSWERS_KEY, {})
        answers[node_id] = choice
        request.session[SESSION_ANSWERS_KEY] = answers

        # Advance to next node
        next_node = choices_dict[choice]["next"]
        request.session[SESSION_NODE_KEY] = next_node

        # Any new path means last event id no longer relevant
        request.session.pop(SESSION_LAST_EVENT_ID, None)

        request.session.modified = True
        return redirect("recommender:question")

    # GET
    choices = [(k, v["label"]) for k, v in node["choices"].items()]
    return render(
        request,
        "recommender/question.html",
        {"node_id": node_id, "question": node["text"], "choices": choices},
    )

def _handle_leaf(request, node_id: str, node: Dict[str, Any]):
    """
    Create RecommendationEvent exactly once for a reached leaf.
    If the user refreshes, we don't create duplicates.
    """
    last_event_id = request.session.get(SESSION_LAST_EVENT_ID)
    if last_event_id:
        # If already logged for this session leaf, just go to it
        return redirect("recommender:result", event_id=last_event_id)

    answers = request.session.get(SESSION_ANSWERS_KEY, {})
    meta = request.session.get(SESSION_META_KEY, {})

    event = RecommendationEvent.objects.create(
        session_key=request.session.session_key,
        answers=answers,
        recommended_products=node.get("products", []),
        product_links=node.get("links", []),
        # store common dimensions if present (optional model fields)
        segment=meta.get("segment", ""),
        customer_type=meta.get("customer_type", ""),
        goal=meta.get("goal", ""),
    )

    request.session[SESSION_LAST_EVENT_ID] = event.id
    request.session.modified = True
    return redirect("recommender:result", event_id=event.id)

def result(request, event_id: int):
    event = RecommendationEvent.objects.get(id=event_id)

    # Pair by index, safe when lengths differ
    products = event.recommended_products or []
    links = event.product_links or []

    products_with_links = []
    for i, name in enumerate(products):
        url = links[i] if i < len(links) else ""
        products_with_links.append({"name": name, "url": url})

    return render(request, "recommender/result.html", {
        "event": event,
        "products_with_links": products_with_links,
    })

def _fig_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=160)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def _pie_chart_base64(counter: Counter, title: str, max_slices: int = 8) -> str:
    # Keep chart readable: top N + "Other"
    items = counter.most_common(max_slices)
    if not items:
        # empty chart placeholder
        fig = plt.figure(figsize=(5, 3))
        plt.title(title)
        plt.text(0.5, 0.5, "No data", ha="center", va="center")
        plt.axis("off")
        return _fig_to_base64(fig)

    labels = [k if k else "(blank)" for k, _ in items]
    sizes = [v for _, v in items]

    remaining = sum(counter.values()) - sum(sizes)
    if remaining > 0:
        labels.append("Other")
        sizes.append(remaining)

    fig = plt.figure(figsize=(5, 4))
    plt.title(title)
    plt.pie(sizes, labels=labels, autopct="%1.0f%%", startangle=90)
    plt.axis("equal")
    return _fig_to_base64(fig)


def _bar_chart_base64(counter: Counter, title: str, top_n: int = 10) -> str:
    items = counter.most_common(top_n)
    if not items:
        fig = plt.figure(figsize=(6, 3))
        plt.title(title)
        plt.text(0.5, 0.5, "No data", ha="center", va="center")
        plt.axis("off")
        return _fig_to_base64(fig)

    labels = [k if k else "(blank)" for k, _ in items]
    values = [v for _, v in items]

    fig = plt.figure(figsize=(8, 4))
    plt.title(title)
    plt.bar(range(len(values)), values)
    plt.xticks(range(len(labels)), labels, rotation=35, ha="right")
    plt.ylabel("Count")
    plt.tight_layout()
    return _fig_to_base64(fig)

@admin_required
def analytics(request):
    """
    Analytics dashboard:
    - KPI cards
    - goal/customer type pie charts
    - top products bar chart
    - recent events table
    """
    qs = RecommendationEvent.objects.order_by("-created_at")
    events = list(qs)

    total = len(events)
    goal_counter = Counter((e.goal or "").strip() for e in events)
    customer_type_counter = Counter((e.customer_type or "").strip() for e in events)
    segment_counter = Counter((e.segment or "").strip() for e in events)

    product_counter = Counter()
    for e in events:
        for p in (e.recommended_products or []):
            p = (p or "").strip()
            if p:
                product_counter[p] += 1

    goal_chart = _pie_chart_base64(goal_counter, "Goals (Business/Individual)")
    customer_type_chart = _pie_chart_base64(customer_type_counter, "Customer Type")
    top_products_chart = _bar_chart_base64(product_counter, "Top Recommended Products", top_n=12)

    # Simple “most common” KPIs
    top_goal = goal_counter.most_common(1)[0][0] if goal_counter else "-"
    top_customer_type = customer_type_counter.most_common(1)[0][0] if customer_type_counter else "-"
    top_product = product_counter.most_common(1)[0][0] if product_counter else "-"

    return render(request, "recommender/analytics.html", {
        "events": events[:200],  # show latest 200 in table
        "kpis": {
            "total": total,
            "top_goal": top_goal or "-",
            "top_customer_type": top_customer_type or "-",
            "top_product": top_product or "-",
        },
        "charts": {
            "goal": goal_chart,
            "customer_type": customer_type_chart,
            "top_products": top_products_chart,
        },
    })

@admin_required
def analytics_detail(request, event_id: int):
    """
    Show one event with:
    - meta fields
    - recommended products + links paired by index
    - answers JSON
    """
    try:
        event = RecommendationEvent.objects.get(id=event_id)
    except RecommendationEvent.DoesNotExist:
        raise Http404("Event not found")

    # Pair by index, safe when lengths differ
    products = event.recommended_products or []
    links = event.product_links or []

    products_with_links = []
    for i, name in enumerate(products):
        url = links[i] if i < len(links) else ""
        products_with_links.append({"name": name, "url": url})

    return render(request, "recommender/analytics_detail.html", {
        "event": event,
        "products_with_links": products_with_links,
    })

def restart(request):
    """
    Convenience endpoint if you want a 'Restart' link.
    """
    _ensure_session(request)
    _reset_flow(request)
    return redirect("recommender:question")
