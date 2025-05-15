from typing import Optional, Tuple

from apps.element.models import Element
from apps.user.models import User


def get_element_by_id_service(
    element_id: str, user: User
) -> Tuple[Optional[Element], Optional[str]]:
    try:
        # Try to find the element
        element = Element.objects.filter(id=element_id).first()

        # If element doesn't exist
        if not element:
            return None, "Element not found"

        # Check if user has access (user is the creator of the element)
        if element.created_by != user:
            return None, "You don't have permission to access this element"

        return element, None
    except Exception as e:
        return None, f"Error retrieving element: {str(e)}"
