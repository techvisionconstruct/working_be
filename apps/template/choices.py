from django.db import models
from django.utils.translation import gettext_lazy as _


class TemplateOrigin(models.TextChoices):
    ORIGINAL = "original", _("Original")
    DERIVED = "derived", _("Derived")


class TemplateStatus(models.TextChoices):
    DRAFT = "draft", _("Draft")
    PUBLISHED = "published", _("Published")
    ARCHIVED = "archived", _("Archived")
