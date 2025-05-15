from django.db import models

from .choices import ProposalStatus
from helpers.generate_short_id import generate_short_id


class Proposal(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Proposal Details
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=ProposalStatus.choices,
        default=ProposalStatus.DRAFT,
    )
    image = models.ImageField(
        upload_to="proposals/images/",
        blank=True,
        null=True,
    )

    # Template Reference
    template = models.ForeignKey(
        "template.Template",
        on_delete=models.SET_NULL,
        related_name="proposals",
        blank=True,
        null=True,
    )

    # Contract Reference
    contract = models.ForeignKey(
        "contract.Contract",
        on_delete=models.SET_NULL,
        related_name="proposals",
        blank=True,
        null=True,
    )

    # Ownership
    owner = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    # Client Information
    client_name = models.CharField(max_length=255, blank=True, null=True)
    client_email = models.EmailField(blank=True, null=True)
    client_phone = models.CharField(max_length=20, blank=True, null=True)
    client_address = models.TextField(blank=True, null=True)

    # Dates
    valid_until = models.DateField(blank=True, null=True)

    # Cost Calculations
    total_material_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True,
    )
    total_labor_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True,
    )
    total_with_markup_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True,
    )
    total_cost = models.DecimalField(
        max_digits=10,
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
        verbose_name = "Proposal"
        verbose_name_plural = "Proposals"
        ordering = ["-created_at"]
        db_table = "proposals"
