from django.db import models

from helpers.generate_short_id import generate_short_id
from .choices import TradeOrigin


class Trade(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Trade Details
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="trades/images/",
        blank=True,
        null=True,
    )

    # Trade Origin
    origin = models.CharField(
        max_length=10,
        choices=TradeOrigin.choices,
        default=TradeOrigin.ORIGINAL,
    )
    source = models.ForeignKey(
        "trade.Trade",
        on_delete=models.CASCADE,
        related_name="source_trade",
        blank=True,
        null=True,
    )

    # Elements
    elements = models.ManyToManyField(
        "element.Element",
        related_name="trades",
        blank=True,
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
        verbose_name = "Trade"
        verbose_name_plural = "Trades"
        ordering = ["-created_at"]
        db_table = "trades"
