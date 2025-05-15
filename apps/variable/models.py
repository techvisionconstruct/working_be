from django.db import models

from helpers.generate_short_id import generate_short_id
from .choices import VariableOrigin


class Variable(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Variable Details
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    formula = models.CharField(max_length=255, blank=True, null=True)
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True,
    )
    is_global = models.BooleanField(default=False)

    # Variable Origin
    origin = models.CharField(
        max_length=10,
        choices=VariableOrigin.choices,
        default=VariableOrigin.ORIGINAL,
    )
    source = models.ForeignKey(
        "variable.Variable",
        on_delete=models.CASCADE,
        related_name="source_variable",
        blank=True,
        null=True,
    )

    # Variable Type
    variable_type = models.ForeignKey(
        "variable_type.VariableType",
        on_delete=models.CASCADE,
        related_name="variables",
        blank=True,
        null=True,
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
        verbose_name = "Variable"
        verbose_name_plural = "Variables"
        ordering = ["-created_at"]
        db_table = "variables"
