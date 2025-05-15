from django.db import models

from .choices import TemplateOrigin, TemplateStatus
from helpers.generate_short_id import generate_short_id


class Template(models.Model):
    id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_short_id,
        unique=True,
    )
    image = models.ImageField(
        upload_to="templates/images/",
        blank=True,
        null=True,
    )

    # Template Details
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=10,
        choices=TemplateStatus.choices,
        default=TemplateStatus.DRAFT,
    )

    # Template Origin
    origin = models.CharField(
        max_length=10,
        choices=TemplateOrigin.choices,
        default=TemplateOrigin.ORIGINAL,
    )
    source = models.ForeignKey(
        "template.Template",
        on_delete=models.CASCADE,
        related_name="source_template",
        blank=True,
        null=True,
    )

    # Ownership
    owner = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="%(class)s_owner",
        blank=True,
        null=True,
    )

    # Template Structure
    trades = models.ManyToManyField(
        "trade.Trade",
        related_name="templates",
        blank=True,
    )
    variables = models.ManyToManyField(
        "variable.Variable",
        related_name="templates",
        blank=True,
    )

    # Flags
    is_public = models.BooleanField(default=False)

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

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"
        ordering = ["-created_at"]
        db_table = "templates"
