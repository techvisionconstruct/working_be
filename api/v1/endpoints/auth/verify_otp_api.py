from ninja import Router
from django.http import HttpRequest
from ninja.responses import Response

from apps.otp.dto import VerifyOTPRequest
from apps.auth.dto import SignUpResponse
from apps.otp.services.verify_otp_service import verify_otp_service
from apps.auth.mappings import SIGNUP_ERROR_MAPPINGS
from handlers.format_signup_error import format_signup_error
from helpers import determine_status_code, map_error_to_fields

router = Router(tags=["Authentication"])


@router.post(
    "/",
    response={
        201: SignUpResponse,
        400: SignUpResponse,
        409: SignUpResponse,
    },
)
def verify_otp_endpoint(request: HttpRequest, payload: VerifyOTPRequest):
    user_data, error = verify_otp_service(
        email=payload.email,
        otp_code=payload.otp_code,
        password=payload.password,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )

    if error:
        # Format error message following the standardized pattern
        formatted_error = format_signup_error(error)

        # Determine appropriate status code
        status_code = determine_status_code(error)

        # Create field-specific errors array using signup-specific mappings
        field_errors = map_error_to_fields(error, SIGNUP_ERROR_MAPPINGS)

        # Create error response with proper status code
        error_response = {
            "success": False,
            "message": formatted_error,
            "errors": field_errors,
            "user": None,
        }

        return Response(error_response, status=status_code)

    # Return successful response
    success_response = {
        "success": True,
        "message": "Registration successful",
        "user": user_data,
    }

    return Response(success_response, status=201)
