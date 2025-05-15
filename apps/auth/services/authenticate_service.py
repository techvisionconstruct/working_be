from typing import Optional, Any
from ninja.security import HttpBearer
from django.http import HttpRequest

from apps.auth.services import authenticate_token_service


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        user, error = authenticate_token_service(token)
        return user
