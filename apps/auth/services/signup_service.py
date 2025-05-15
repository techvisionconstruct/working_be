from typing import Dict, Optional, Tuple
import re

from apps.user.services import create_user_service
from apps.otp.services.send_otp_service import send_otp_service


def signup_service(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    username: Optional[str] = None,
) -> Tuple[Optional[Dict], Optional[str]]:
    # Validate required fields
    if not email:
        return None, "Email is required"

    if not password:
        return None, "Password is required"

    if not first_name:
        return None, "First name is required"

    if not last_name:
        return None, "Last name is required"

    # Email format validation
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        return None, "Invalid email format"

    # Password strength validation
    if len(password) < 8:
        return None, "Password must be at least 8 characters"

    has_number = any(char.isdigit() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    if not (has_number and has_uppercase):
        return (
            None,
            "Password must contain at least one number and one uppercase letter",
        )

    # Generate and send OTP
    otp, error = send_otp_service(email=email)

    if error:
        return None, f"Error sending verification code: {error}"

    # Return response indicating OTP has been sent
    response_data = {
        "message": "Verification code sent to your email",
        "email": email,
        "requires_verification": True,
    }

    # Store user details temporarily (in real implementation, you might want to store these
    # in a secure way like session or encrypted in a database)

    return response_data, None
