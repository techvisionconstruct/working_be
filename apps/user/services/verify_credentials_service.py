from typing import Optional
from django.contrib.auth import authenticate
from apps.user.models import User


def verify_credentials_service(email: str, password: str) -> Optional[User]:
    user = authenticate(username=email, password=password)
    return user
