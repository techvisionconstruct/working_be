from django.utils import timezone
from apps.user.models import User


def update_last_login_service(user: User) -> User:
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])
    return user
