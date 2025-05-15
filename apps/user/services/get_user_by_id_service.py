from typing import Optional
from apps.user.models import User


def get_user_by_id_service(user_id: str) -> Optional[User]:
    # Check if the user ID is valid
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
