from django.db import models
from django.db import models

from helpers.generate_short_id import generate_short_id


class Product(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Product Details
    search_term = models.CharField(max_length=255, blank=False, null=False)
    source_platform = models.CharField(max_length=255, blank=False, null=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    item_id = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(max_length=1000, blank=True, null=True)
    primary_image = models.URLField(max_length=1000, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    ratings_total = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)

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
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]
        db_table = "products"
