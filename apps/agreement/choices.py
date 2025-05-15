from django.db import models
from django.utils.translation import gettext_lazy as _


class AgreementType(models.TextChoices):
    TERMS = "terms", _("Terms")
    PRIVACY = "privacy", _("Privacy")
    COOKIE = "cookie", _("Cookie")
    OTHER = "other", _("Other")
