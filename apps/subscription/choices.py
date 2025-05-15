from django.db import models
from django.utils.translation import gettext_lazy as _


class SubscriptionStatus(models.TextChoices):
    ACTIVE = "active", _("Active")
    INACTIVE = "inactive", _("Inactive")
    PENDING = "pending", _("Pending")
    CANCELED = "canceled", _("Canceled")
    EXPIRED = "expired", _("Expired")
    TRIAL = "trial", _("Trial")


class SubscriptionType(models.TextChoices):
    FREE = "free", _("Free")
    PAID = "paid", _("Paid")
    TRIAL = "trial", _("Trial")
    GIFT = "gift", _("Gift")
