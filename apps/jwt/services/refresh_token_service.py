from typing import Dict, Optional, Tuple


from apps.jwt.services import (
    verify_refresh_token_service,
    generate_tokens_service,
    save_tokens_service,
)

from apps.jwt.services.delete_token_by_refresh_token_service import (
    delete_token_by_refresh_token_service,
)
from apps.user.services import get_user_by_id_service


def refresh_token_service(refresh_token: str) -> Tuple[Optional[Dict], Optional[str]]:
    try:
        # Verify the refresh token
        payload = verify_refresh_token_service(refresh_token)

        if not payload:
            return None, "Invalid refresh token"

        # Get user from verified token
        user_id = payload.get("user_id")
        if not user_id:
            return None, "Invalid token payload"

        user = get_user_by_id_service(user_id)

        if not user:
            return None, "User not found"

        if not user.is_active:
            return None, "User account is inactive"

        # Delete the old refresh token
        try:
            delete_token_by_refresh_token_service(user, refresh_token)
        except Exception as e:
            return None, f"Error invalidating old refresh token: {str(e)}"

        # Generate new tokens
        try:
            access_token, new_refresh_token, access_expires_at, refresh_expires_at = (
                generate_tokens_service(user)
            )
        except Exception as e:
            return None, f"Error generating new authentication tokens: {str(e)}"

        # Save new tokens in database
        try:
            save_tokens_service(
                user,
                access_token,
                new_refresh_token,
                access_expires_at,
                refresh_expires_at,
            )
        except Exception as e:
            return None, f"Error saving new authentication tokens: {str(e)}"

        # Create response data
        tokens_data = {
            "token_type": "Bearer",
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "access_token_expires_at": access_expires_at.isoformat(),
            "refresh_token_expires_at": refresh_expires_at.isoformat(),
        }

        return {"tokens": tokens_data}, None

    except Exception as e:
        return None, f"Token refresh error: {str(e)}"
