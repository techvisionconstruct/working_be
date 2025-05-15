from ninja import Router, Path
from django.http import HttpRequest

from apps.user.dto import AdminUserDetailResponse
from apps.user.services.admin import admin_get_user_by_id_service
from apps.user.choices import UserRole
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["User Management"])


@router.get("/{user_id}/", response=AdminUserDetailResponse, auth=AuthBearer())
def admin_get_user_by_id_api(
    request: HttpRequest, user_id: str = Path(..., description="User ID")
):
    # Check admin privileges
    if not request.auth or request.auth.role != UserRole.ADMIN:
        return {
            "success": False,
            "message": "Failed to retrieve user. Insufficient permissions.",
            "errors": [
                {
                    "field": "general",
                    "message": "Only administrators can view user details",
                }
            ],
            "data": None,
        }

    # Call service to get user
    user_data, error = admin_get_user_by_id_service(
        admin_user=request.auth,
        user_id=user_id,
    )

    # Handle error response
    if error:
        status_message = "User not found" if "not found" in error else error
        return {
            "success": False,
            "message": f"Failed to retrieve user. {status_message}",
            "errors": [{"field": "general", "message": error}],
            "data": None,
        }

    # Success response
    return {
        "success": True,
        "message": "Successfully retrieved user details",
        "errors": [],
        "data": user_data,
    }
