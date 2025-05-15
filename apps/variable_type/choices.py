from django.db import models
from django.utils.translation import gettext_lazy as _


class VariableTypeCategory(models.TextChoices):
    LENGTH = "length", _("Length")
    AREA = "area", _("Area")
    VOLUME = "volume", _("Volume")
    COUNT = "count", _("Count")
    WEIGHT = "weight", _("Weight")
    CUSTOM = "custom", _("Custom")
    CURRENCY = "currency", _("Currency")
