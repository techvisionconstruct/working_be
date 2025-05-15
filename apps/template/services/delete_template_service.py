from typing import Optional, Tuple

from apps.template.models import Template
from apps.user.models import User


def delete_template_service(template_id: str, user: User) -> Tuple[bool, Optional[str]]:
    try:
        # Check if the template exists
        try:
            template = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return False, f"Template with ID {template_id} not found."

        # Check permissions - only allow template creator, owner, or staff to delete
        if template.created_by != user and template.owner != user and not user.is_staff:
            return False, "You don't have permission to delete this template."

        # Check if the template is used as a source for derived templates
        derived_templates = Template.objects.filter(source_id=template)
        if derived_templates.exists():
            return (
                False,
                "Cannot delete this template as it is used as a source for derived templates.",
            )

        # Record the user who performed the deletion
        template.updated_by = user

        # Delete the template
        template.delete()

        return True, None
    except Exception as e:
        return False, f"Error deleting template: {str(e)}"
