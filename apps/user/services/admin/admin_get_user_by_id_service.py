from typing import Dict, Optional, Tuple

from apps.user.models import User
from apps.user.choices import UserRole


def admin_get_user_by_id_service(
    admin_user: User,
    user_id: str,
) -> Tuple[Optional[Dict], Optional[str]]:
    # Verify admin privileges
    if admin_user.role != UserRole.ADMIN and not admin_user.is_superuser:
        return None, "Permission denied: Only administrators can view user details"

    try:
        # Get the user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None, f"User with ID {user_id} not found"

        # Get creator info if available
        creator = None
        if hasattr(user, "created_by") and user.created_by:
            creator = {
                "id": user.created_by.id,
                "email": user.created_by.email,
                "username": user.created_by.username,
                "first_name": user.created_by.first_name,
                "last_name": user.created_by.last_name,
                "role": user.created_by.role,
            }

        # Create user data
        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "created_by": creator,
        }

        return user_data, None

    except Exception as e:
        return None, f"Error retrieving user: {str(e)}"
