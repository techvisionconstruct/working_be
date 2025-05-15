from typing import Optional, Tuple
from django.db import transaction

from apps.user.models import User
from apps.user.choices import UserRole


def create_user_service(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    username: Optional[str] = None,
    role: str = UserRole.USER,
) -> Tuple[Optional[User], Optional[str]]:
    try:
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return None, "Email already registered"

        # Create user with transaction to ensure atomicity
        with transaction.atomic():
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                username=username,
                role=role,
            )

            return user, None
    except Exception as e:
        return None, str(e)
