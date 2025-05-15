from django.db import models

from helpers.generate_short_id import generate_short_id


class JWTToken(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # Token Details
    access_token = models.CharField(max_length=255, unique=True)
    refresh_token = models.CharField(max_length=255, unique=True)
    access_token_expires_at = models.DateTimeField()
    refresh_token_expires_at = models.DateTimeField()
    token_type = models.CharField(
        default="Bearer",
        max_length=10,
        blank=False,
        null=False,
    )

    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "JWT Token"
        verbose_name_plural = "JWT Tokens"
        ordering = ["-created_at"]
        db_table = "jwt_tokens"
