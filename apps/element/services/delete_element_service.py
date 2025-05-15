from typing import Optional, Tuple

from apps.element.models import Element
from apps.user.models import User


def delete_element_service(element_id: str, user: User) -> Tuple[bool, Optional[str]]:
    try:
        # Check if the element exists
        try:
            element = Element.objects.get(id=element_id)
        except Element.DoesNotExist:
            return False, f"Element with ID {element_id} not found."

        # Check permissions
        if element.created_by != user and not user.is_staff:
            return False, "You don't have permission to delete this element"

        element.delete()
        return True, None
    except Exception as e:
        return False, f"Error deleting element: {str(e)}"
