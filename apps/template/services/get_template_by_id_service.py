from typing import Optional, Tuple

from apps.template.models import Template
from apps.user.models import User


def get_template_by_id_service(
    template_id: str, user: User
) -> Tuple[Optional[Template], Optional[str]]:
    try:
        # Try to find the template
        template = Template.objects.filter(id=template_id).first()

        # If template doesn't exist
        if not template:
            return None, "Template not found"

        # Check if user has access (user is owner or template is public)
        if template.created_by != user and not template.is_public:
            return None, "You don't have permission to access this template"

        return template, None
    except Exception as e:
        return None, f"Error retrieving template: {str(e)}"
