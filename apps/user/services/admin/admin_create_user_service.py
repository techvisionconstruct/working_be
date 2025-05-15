from typing import Optional, Tuple, Dict
from django.db import transaction

from apps.user.models import User
from apps.user.choices import UserRole


def admin_create_user_service(
    admin_user: User,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    username: Optional[str] = None,
    role: str = UserRole.USER,
    is_active: bool = True,
    is_staff: bool = False,
    is_superuser: bool = False,
) -> Tuple[Optional[Dict], Optional[str]]:
    if admin_user.role != UserRole.ADMIN and not admin_user.is_superuser:
        return None, "Permission denied: Only administrators can create users"
    try:
        if User.objects.filter(email=email).exists():
            return None, "Email already registered"

        with transaction.atomic():
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                username=username,
                role=role,
                is_active=is_active,
                is_staff=is_staff,
                is_superuser=is_superuser,
            )

            user.created_by = admin_user
            user.save()

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
                "created_by": admin_user.id,
            }

            return user_data, None

    except Exception as e:
        return None, f"Error creating user: {str(e)}"
