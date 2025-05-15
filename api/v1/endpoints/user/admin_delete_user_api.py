from ninja import Router, Path
from django.http import HttpRequest

from apps.user.dto import AdminUserDeleteResponse
from apps.user.services.admin import admin_delete_user_service
from apps.user.choices import UserRole
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["User Management"])


@router.delete("/{user_id}/", response=AdminUserDeleteResponse, auth=AuthBearer())
def admin_delete_user_api(
    request: HttpRequest, user_id: str = Path(..., description="User ID")
):
    # Check if user is authenticated and has admin privileges
    if not request.auth or request.auth.role != UserRole.ADMIN:
        return {
            "success": False,
            "message": "Failed to delete user. Insufficient permissions.",
            "errors": [
                {"field": "general", "message": "Only administrators can delete users"}
            ],
            "data": None,
        }

    # Call service to delete user
    user_data, error = admin_delete_user_service(
        admin_user=request.auth,
        user_id=user_id,
    )

    # Handle error response
    if error:
        status_message = "User not found" if "not found" in error else error

        return {
            "success": False,
            "message": f"Failed to delete user. {status_message}",
            "errors": [{"field": "general", "message": error}],
            "data": None,
        }

    # Success response
    return {
        "success": True,
        "message": "Successfully deleted user",
        "errors": [],
        "data": None,
    }
