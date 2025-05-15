from django.db import models
from django.utils import timezone
from helpers.generate_short_id import generate_short_id


class OTP(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def is_valid(self):
        """Check if the OTP is still valid (not expired and not verified)"""
        return not self.is_verified and self.expires_at > timezone.now()

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
        ordering = ["-created_at"]
        db_table = "otps"
