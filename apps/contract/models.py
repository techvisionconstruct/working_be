from django.db import models

from .choices import ContractStatus
from helpers.generate_short_id import generate_short_id


class Contract(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Contract Details
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=ContractStatus.choices,
        default=ContractStatus.DRAFT,
    )
    terms = models.TextField(blank=True, null=True)

    # Signatures
    client_initials = models.CharField(max_length=10, blank=True, null=True)
    client_signature = models.ImageField(
        upload_to="signatures/clients/", blank=True, null=True
    )
    client_signed_at = models.DateTimeField(blank=True, null=True)

    contractor_initials = models.CharField(max_length=10, blank=True, null=True)
    contractor_signature = models.ImageField(
        upload_to="signatures/contractors/", blank=True, null=True
    )
    contractor_signed_at = models.DateTimeField(blank=True, null=True)

    # Ownership
    owner = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
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
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ["-created_at"]
        db_table = "contracts"
