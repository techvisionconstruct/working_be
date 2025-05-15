from django.db import models
from django.conf import settings

from helpers.generate_short_id import generate_short_id


class Industry(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Industry Information
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"
        ordering = ["-created_at"]
        db_table = "industries"
