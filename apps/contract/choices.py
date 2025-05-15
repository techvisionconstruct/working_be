from django.db import models
from django.utils.translation import gettext_lazy as _


class ContractStatus(models.TextChoices):
    DRAFT = "draft", _("Draft")
    PUBLISHED = "published", _("Published")
    ARCHIVED = "archived", _("Archived")
