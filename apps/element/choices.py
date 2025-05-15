from django.db import models
from django.utils.translation import gettext_lazy as _


class ElementOrigin(models.TextChoices):
    ORIGINAL = "original", _("Original")
    DERIVED = "derived", _("Derived")
