from django.db import models
from django.contrib import admin

class RecommendationEvent(models.Model):
    """
    A log row created exactly when the user reaches a leaf (final answer).
    No PII stored; only session key + answers + recommended products.
    """

    created_at = models.DateTimeField(auto_now_add=True)

    # helps you dedupe / group events without storing identity
    session_key = models.CharField(max_length=64, db_index=True)

    # store everything you need for later analysis
    answers = models.JSONField()  # { "q1": "...", "q2": "...", ... }
    recommended_products = models.JSONField()  # ["KPR BTN Platinum", ...]
    product_links = models.JSONField(default=list, blank=True)  # optional

    # optional “dimensions” to filter quickly
    segment = models.CharField(max_length=32, blank=True)  # "konven"
    customer_type = models.CharField(max_length=32, blank=True)  # "individual" / "business"
    goal = models.CharField(max_length=64, blank=True)  # "property" / "saving" / etc.

    def __str__(self) -> str:
        return f"{self.created_at:%Y-%m-%d %H:%M} | {self.segment} | {self.customer_type}"

admin.site.register(RecommendationEvent)