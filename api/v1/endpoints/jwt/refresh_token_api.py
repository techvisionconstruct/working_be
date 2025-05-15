from ninja import Router
from django.http import HttpRequest
from ninja.responses import Response

from apps.auth.dto import RefreshTokenRequest, RefreshTokenResponse
from apps.jwt.services import refresh_token_service

router = Router(tags=["JWT"])


@router.post(
    "/",
    response={
        200: RefreshTokenResponse,
        400: RefreshTokenResponse,
        401: RefreshTokenResponse,
    },
)
def refresh_token_endpoint(request: HttpRequest, payload: RefreshTokenRequest):
    # Process the refresh token request
    tokens_data, error = refresh_token_service(payload.refresh_token)

    # Handle error cases
    if error:
        status_code = (
            401 if "invalid" in error.lower() or "expired" in error.lower() else 400
        )

        error_response = {
            "success": False,
            "message": f"Failed to refresh token: {error}",
            "errors": [{"field": "refresh_token", "message": error}],
            "tokens": None,
        }

        return Response(error_response, status=status_code)

    # Return successful response
    response_data = {
        "success": True,
        "message": "Successfully refreshed tokens",
        "errors": [],
        "tokens": tokens_data["tokens"],
    }

    return response_data
