from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    ADMIN = "admin", _("Admin")
    USER = "user", _("User")
    CLIENT = "client", _("Client")
    CONTRACTOR = "contractor", _("Contractor")
