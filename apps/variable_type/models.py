from django.db import models

from .choices import VariableTypeCategory
from helpers.generate_short_id import generate_short_id


class VariableType(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Variable Type Details
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=10,
        choices=VariableTypeCategory.choices,
        default=VariableTypeCategory.CUSTOM,
    )
    unit = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    is_built_in = models.BooleanField(default=False)

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
        verbose_name = "Variable Type"
        verbose_name_plural = "Variable Types"
        ordering = ["-created_at"]
        db_table = "variable_types"
