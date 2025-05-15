import datetime

from apps.jwt.models import JWTToken
from apps.user.models import User


def save_tokens_service(
    user: User,
    access_token: str,
    refresh_token: str,
    access_expires_at: datetime.datetime,
    refresh_expires_at: datetime.datetime,
) -> JWTToken:
    # Delete all existing tokens for this user
    JWTToken.objects.filter(user=user).delete()

    # Create a new token record
    token = JWTToken.objects.create(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expires_at=access_expires_at,
        refresh_token_expires_at=refresh_expires_at,
    )

    return token
