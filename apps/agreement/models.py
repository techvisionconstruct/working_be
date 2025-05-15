from django.db import models
from django.conf import settings

from helpers.generate_short_id import generate_short_id
from .choices import AgreementType


class Agreement(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Agreement Details
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField()
    version = models.CharField(max_length=20, blank=False, null=False)
    agreement_type = models.CharField(
        max_length=20,
        choices=AgreementType.choices,
        default=AgreementType.OTHER,
    )

    # Status
    is_active = models.BooleanField(default=True)

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Agreement"
        verbose_name_plural = "Agreements"
        ordering = ["-created_at"]
        db_table = "agreements"
