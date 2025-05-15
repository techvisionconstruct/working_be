from ninja import Router
from django.http import HttpRequest
from ninja.responses import Response

from apps.auth.services.signout_service import signout_service
from apps.auth.dto import SignOutResponse
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Authentication"])


@router.post(
    "/",
    response={200: SignOutResponse, 401: SignOutResponse},
    auth=AuthBearer(),
)
def signout_endpoint(request: HttpRequest):
    user = request.auth
    # Extract access token from Authorization header
    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        return Response(
            {
                "success": False,
                "message": "No valid access token provided.",
                "errors": [{"field": "token", "message": "Missing or invalid token"}],
                "user": None,
                "tokens": None,
            },
            status=401,
        )
    access_token = auth_header.split(" ", 1)[1]

    # Call the signout service
    error = signout_service(user, access_token)

    if error:
        return Response(
            {
                "success": False,
                "message": "Failed to sign out.",
                "errors": [{"field": "general", "message": str(error)}],
                "user": None,
                "tokens": None,
            },
            status=400,
        )

    return {
        "success": True,
        "message": "Successfully signed out.",
        "errors": [],
        "user": None,
        "tokens": None,
    }
