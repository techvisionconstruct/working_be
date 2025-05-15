from django.db import models

from helpers.generate_short_id import generate_short_id
from .choices import ElementOrigin


class Element(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Element Details
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    # Element Origin
    origin = models.CharField(
        max_length=10,
        choices=ElementOrigin.choices,
        default=ElementOrigin.ORIGINAL,
    )
    source = models.ForeignKey(
        "element.Element",
        on_delete=models.CASCADE,
        related_name="source_element",
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to="elements/images/",
        blank=True,
        null=True,
    )

    # Cost Formulas
    material_cost_formula = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    material_formula_variables = models.JSONField(
        blank=True,
        null=True,
    )
    labor_cost_formula = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    labor_formula_variables = models.JSONField(
        blank=True,
        null=True,
    )
    material_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True,
    )
    labor_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True,
    )
    markup = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
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
        verbose_name = "Element"
        verbose_name_plural = "Elements"
        ordering = ["-created_at"]
        db_table = "elements"
