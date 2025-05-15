from typing import Optional, Tuple
from django.utils import timezone

from apps.otp.models import OTP
from apps.user.services import create_user_service


def verify_otp_service(
    email: str,
    otp_code: str,
    password: str,
    first_name: str,
    last_name: str,
) -> Tuple[Optional[dict], Optional[str]]:
    try:
        # Find the latest OTP for this email
        otp = OTP.objects.filter(email=email).first()

        if not otp:
            return None, "No verification code found for this email"

        if otp.is_verified:
            return None, "Verification code already used"

        if otp.expires_at < timezone.now():
            return None, "Verification code has expired"

        if otp.code != otp_code:
            return None, "Invalid verification code"

        # Mark OTP as verified
        otp.is_verified = True
        otp.save()

        # Create the user
        user, error = create_user_service(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        if error:
            return None, error

        # Create response data
        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
            "is_active": user.is_active,
        }

        return user_data, None
    except Exception as e:
        return None, str(e)
