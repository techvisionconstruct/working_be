from typing import Optional, Tuple
from django.core.mail import send_mail
from django.conf import settings

from apps.otp.models import OTP
from helpers.generate_otp import generate_otp, get_otp_expiry_time


def send_otp_service(email: str) -> Tuple[Optional[OTP], Optional[str]]:
    """
    Generate an OTP, save it, and send it to the user's email
    Returns the OTP object and any error message
    """
    try:
        # Generate a new 6-digit OTP
        otp_code = generate_otp(6)
        expires_at = get_otp_expiry_time(10)  # OTP expires in 10 minutes

        # Delete any existing OTPs for this email (if any)
        OTP.objects.filter(email=email).delete()

        # Create new OTP record
        otp = OTP.objects.create(email=email, code=otp_code, expires_at=expires_at)

        # Send email with OTP
        subject = "Your Verification Code"
        message = f"Your verification code is: {otp_code}\n\nThis code will expire in 10 minutes."
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, email_from, recipient_list)

        return otp, None
    except Exception as e:
        return None, str(e)
