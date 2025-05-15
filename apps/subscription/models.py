from django.db import models


from apps.subscription.choices import SubscriptionStatus, SubscriptionType
from helpers.generate_short_id import generate_short_id


class Subscription(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    user = models.OneToOneField(
        "user.User",
        on_delete=models.CASCADE,
        related_name="subscription",
    )

    # Subscription Details
    plan = models.ForeignKey(
        "subscription_plan.SubscriptionPlan",
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )
    status = models.CharField(
        max_length=20,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.ACTIVE,
    )
    subscription_type = models.CharField(
        max_length=20,
        choices=SubscriptionType.choices,
        default=SubscriptionType.FREE,
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    # Flags
    is_auto_renew = models.BooleanField(default=True)

    # Payment Information
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    last_payment_date = models.DateTimeField(null=True, blank=True)
    last_payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    next_payment_date = models.DateTimeField(null=True, blank=True)
    next_payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    payment_status = models.CharField(
        max_length=20,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.PENDING,
    )

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
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ["-created_at"]
        db_table = "subscriptions"
