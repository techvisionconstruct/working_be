from typing import Optional, Tuple
from apps.user.models import User

from apps.jwt.services import verify_token_service
from apps.user.services import get_user_by_id_service


def authenticate_token_service(token: str) -> Tuple[Optional[User], Optional[str]]:
    try:
        # verify_token returns the decoded payload directly, not a tuple
        payload = verify_token_service(token)

        if not payload:
            return None, "Invalid token"

        # Get user from verified token - using 'user_id' not 'sub'
        user_id = payload.get("user_id")
        if not user_id:
            return None, "Invalid token payload"

        user = get_user_by_id_service(user_id)

        if not user:
            return None, "User not found"

        if not user.is_active:
            return None, "User account is inactive"

        # Return user if everything is valid
        return user, None
    except Exception as e:
        return None, f"Authentication error: {str(e)}"
