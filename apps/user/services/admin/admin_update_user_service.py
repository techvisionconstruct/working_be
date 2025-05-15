from typing import Dict, Optional, Tuple
from django.db import transaction

from apps.user.models import User
from apps.user.choices import UserRole


def admin_update_user_service(
    admin_user: User,
    user_id: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    username: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_staff: Optional[bool] = None,
    is_superuser: Optional[bool] = None,
    password: Optional[str] = None,
) -> Tuple[Optional[Dict], Optional[str]]:
    # Verify admin privileges
    if admin_user.role != UserRole.ADMIN and not admin_user.is_superuser:
        return None, "Permission denied: Only administrators can update users"

    try:
        # Find the user to update
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None, f"User with ID {user_id} not found"

        # Verify email uniqueness if changing email
        if email and email != user.email and User.objects.filter(email=email).exists():
            return None, "Email already registered to another user"

        # Use transaction to ensure all updates succeed or fail together
        with transaction.atomic():
            # Update fields if provided (not None)
            if email is not None:
                user.email = email

            if first_name is not None:
                user.first_name = first_name

            if last_name is not None:
                user.last_name = last_name

            if username is not None:
                user.username = username

            if role is not None:
                user.role = role

            if is_active is not None:
                user.is_active = is_active

            if is_staff is not None:
                user.is_staff = is_staff

            if is_superuser is not None:
                user.is_superuser = is_superuser

            # Special handling for password
            if password is not None:
                user.set_password(password)

            # Record who updated this user
            user.updated_by = admin_user

            # Save the changes
            user.save()

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

            # Get updater info
            updater = {
                "id": admin_user.id,
                "email": admin_user.email,
                "username": admin_user.username,
                "first_name": admin_user.first_name,
                "last_name": admin_user.last_name,
                "role": admin_user.role,
            }

            # Prepare response data
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
                "updated_by": updater,
            }

            return user_data, None

    except Exception as e:
        return None, f"Error updating user: {str(e)}"
