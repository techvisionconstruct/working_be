from django.db import models
from django.conf import settings

from helpers.generate_short_id import generate_short_id
from apps.agreement.models import Agreement


class UserAgreement(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_agreements",
    )
    agreement = models.ForeignKey(
        Agreement, on_delete=models.CASCADE, related_name="user_acceptances"
    )

    # Acceptance details
    accepted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Agreement"
        verbose_name_plural = "User Agreements"
        ordering = ["-accepted_at"]
        db_table = "user_agreements"
