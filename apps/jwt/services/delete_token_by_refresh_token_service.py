from apps.jwt.models import JWTToken
from apps.user.models import User


def delete_token_by_refresh_token_service(user: User, refresh_token: str) -> bool:
    try:
        token = JWTToken.objects.get(user=user, refresh_token=refresh_token)
        token.delete()
        return True
    except JWTToken.DoesNotExist:
        return False
