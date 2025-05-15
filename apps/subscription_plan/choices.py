from django.db import models
from django.utils.translation import gettext_lazy as _


class SubscriptionPeriod(models.TextChoices):
    MONTHLY = "monthly", _("Monthly")
    QUARTERLY = "quarterly", _("Quarterly")
    SEMI_ANNUALLY = "semi_annually", _("Semi-Annually")
    ANNUALLY = "annually", _("Annually")
    LIFETIME = "lifetime", _("Lifetime")
