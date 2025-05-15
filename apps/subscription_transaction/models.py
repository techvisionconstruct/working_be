from django.db import models

from helpers.generate_short_id import generate_short_id


class SubscriptionTransaction(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Transaction Details
    subscription = models.ForeignKey(
        "subscription.Subscription",
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    transaction_id = models.CharField(
        max_length=100, unique=True, blank=True, null=True
    )

    # Flags
    is_successful = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)

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
        verbose_name = "Subscription Transaction"
        verbose_name_plural = "Subscription Transactions"
        ordering = ["-created_at"]
        db_table = "subscription_transactions"
