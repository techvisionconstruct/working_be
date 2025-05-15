from ninja import Router
from django.http import HttpRequest
from ninja.responses import Response

from apps.auth.dto import SignInRequest, SignInResponse
from apps.auth.services import signin_service
from apps.auth.mappings import SIGNIN_ERROR_MAPPINGS
from handlers.format_signin_error import format_signin_error
from helpers import determine_status_code, map_error_to_fields


router = Router(tags=["Authentication"])


@router.post(
    "/",
    response={
        200: SignInResponse,
        400: SignInResponse,
        401: SignInResponse,
        403: SignInResponse,
    },
)
def signin_endpoint(request: HttpRequest, payload: SignInRequest):
    # Process the sign-in request
    auth_data, error = signin_service(payload.email, payload.password)

    # Handle error cases with standardized messages
    if error:
        # Format error message following the standardized pattern
        formatted_error = format_signin_error(error)

        # Determine appropriate status code
        status_code = determine_status_code(error)

        # Create field-specific errors array using auth-specific mappings
        field_errors = map_error_to_fields(error, SIGNIN_ERROR_MAPPINGS)

        # Create error response with proper status code
        error_response = {
            "success": False,
            "message": formatted_error,
            "errors": field_errors,
            "user": None,
            "tokens": None,
        }

        return Response(error_response, status=status_code)

    # Ensure token_type is set
    if "token_type" not in auth_data["tokens"]:
        auth_data["tokens"]["token_type"] = "Bearer"

    # Return successful response
    response_data = {
        "success": True,
        "message": "Successfully authenticated user",
        "user": auth_data["user"],
        "tokens": auth_data["tokens"],
    }

    return response_data
