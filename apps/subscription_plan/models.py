from django.db import models


from apps.subscription_plan.choices import SubscriptionPeriod
from helpers.generate_short_id import generate_short_id


class SubscriptionPlan(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Subscription Plan Details
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
    )
    period = models.CharField(
        max_length=20,
        choices=SubscriptionPeriod.choices,
        default=SubscriptionPeriod.MONTHLY,
    )
    duration_days = models.PositiveIntegerField(
        default=30,
        blank=False,
        null=False,
    )

    # Flags
    is_active = models.BooleanField(default=True)

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="%(class)s_updated_by",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plans"
        ordering = ["price"]
        db_table = "subscription_plans"
