import re
from typing import Dict, Optional, Tuple
from django.utils import timezone

from apps.user.services import (
    verify_credentials_service,
    update_signin_status_service,
    update_last_login_service,
)
from apps.jwt.services import generate_tokens_service, save_tokens_service


def signin_service(email: str, password: str) -> Tuple[Optional[Dict], Optional[str]]:
    # Input validation
    if not email:
        return None, "Email is required"

    if not password:
        return None, "Password is required"

    # Email format validation
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        return None, "Invalid email format"

    # Verify credentials
    user = verify_credentials_service(email, password)

    if not user:
        return None, "Invalid credentials"

    # Account status checks
    if not user.is_active:
        return None, "User account is disabled"

    if user.is_blocked:
        return None, "User account is blocked"

    if user.is_suspended:
        return None, "User account is suspended"

    # Update sign in status
    try:
        update_signin_status_service(user, True)
    except Exception as e:
        # Log the error but don't fail the signin
        print(f"Error updating signin status: {str(e)}")

    # Update last login
    try:
        update_last_login_service(user)
    except Exception as e:
        # Log the error but don't fail the signin
        print(f"Error updating last login: {str(e)}")

    # Generate tokens
    try:
        access_token, refresh_token, access_expires_at, refresh_expires_at = (
            generate_tokens_service(user)
        )
    except Exception as e:
        return None, f"Error generating authentication tokens: {str(e)}"

    # Save tokens in database
    try:
        save_tokens_service(
            user,
            access_token,
            refresh_token,
            access_expires_at,
            refresh_expires_at,
        )
    except Exception as e:
        return None, f"Error saving authentication tokens: {str(e)}"

    # Prepare subscription data if exists
    subscription_data = None
    if hasattr(user, "subscription"):
        try:
            subscription = user.subscription
            if subscription:
                subscription_data = {
                    "id": subscription.id,
                    "status": subscription.status,
                    "subscription_type": subscription.subscription_type,
                    "start_date": subscription.start_date,
                    "end_date": subscription.end_date,
                    "is_auto_renew": subscription.is_auto_renew,
                    "plan_id": subscription.plan.id if subscription.plan else None,
                    "plan_name": subscription.plan.name if subscription.plan else None,
                }
        except Exception:
            # Handle case where subscription might exist but is invalid
            pass

    # Create response data
    auth_data = {
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            "subscription": subscription_data,
        },
        "tokens": {
            "token_type": "Bearer",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_token_expires_at": access_expires_at.isoformat(),
            "refresh_token_expires_at": refresh_expires_at.isoformat(),
        },
    }

    return auth_data, None
