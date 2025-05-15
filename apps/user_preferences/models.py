from django.db import models

from helpers.generate_short_id import generate_short_id


class UserPreferences(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )

    # User Preferences
    user = models.OneToOneField(
        "user.User",
        on_delete=models.CASCADE,
        related_name="preferences",
        null=True,
        blank=True,
    )

    # Notification Preferences
    email_notifications = models.BooleanField(default=True)
    team_invite_notifications = models.BooleanField(default=True)

    # Document Preferences
    default_currency = models.CharField(max_length=10, default="USD")

    # Regional Preferences
    timezone = models.CharField(max_length=50, default="UTC")
    language = models.CharField(max_length=10, default="en")
    date_format = models.CharField(max_length=10, default="YYYY-MM-DD")

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
        return f"Preferences for {self.id}"

    class Meta:
        verbose_name = "User Preferences"
        verbose_name_plural = "User Preferences"
        ordering = ["-created_at"]
        db_table = "user_preferences"
