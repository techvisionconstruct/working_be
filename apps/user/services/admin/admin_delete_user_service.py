from typing import Dict, Optional, Tuple

from apps.user.models import User
from apps.user.choices import UserRole


def admin_delete_user_service(
    admin_user: User,
    user_id: str,
) -> Tuple[Optional[Dict], Optional[str]]:
    # Verify admin privileges
    if admin_user.role != UserRole.ADMIN and not admin_user.is_superuser:
        return None, "Permission denied: Only administrators can delete users"

    try:
        # Find the user to delete
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None, f"User with ID {user_id} not found"

        # Prevent self-deletion
        if user.id == admin_user.id:
            return None, "Cannot delete your own account"

        # Store user data before deletion for response
        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        }

        user.delete()

        return user_data, None

    except Exception as e:
        return None, f"Error deleting user: {str(e)}"
