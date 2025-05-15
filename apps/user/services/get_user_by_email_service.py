from typing import Optional
from apps.user.models import User


def get_user_by_email_service(email: str) -> Optional[User]:
    # Check if the email is valid
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None
