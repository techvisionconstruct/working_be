from ninja import Router, Path
from django.http import HttpRequest
from typing import Optional

from apps.user.dto import AdminUserDetailResponse, AdminUpdateUserRequest
from apps.user.services.admin import admin_update_user_service
from apps.user.choices import UserRole
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["User Management"])


@router.put("/{user_id}/", response=AdminUserDetailResponse, auth=AuthBearer())
def admin_update_user_api(
    request: HttpRequest,
    payload: AdminUpdateUserRequest,
    user_id: str = Path(..., description="User ID"),
):
    # Check if user is authenticated and has admin privileges
    if not request.auth or request.auth.role != UserRole.ADMIN:
        return {
            "success": False,
            "message": "Failed to update user. Insufficient permissions.",
            "errors": [
                {"field": "general", "message": "Only administrators can update users"}
            ],
            "data": None,
        }

    # Call service to update user
    user_data, error = admin_update_user_service(
        admin_user=request.auth,
        user_id=user_id,
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
        username=payload.username,
        role=payload.role,
        is_active=payload.is_active,
        is_staff=payload.is_staff,
        is_superuser=payload.is_superuser,
        password=payload.password,
    )

    # Handle error response
    if error:
        status_message = "User not found" if "not found" in error else error
        error_field = "email" if "Email already registered" in error else "general"

        return {
            "success": False,
            "message": f"Failed to update user. {status_message}",
            "errors": [{"field": error_field, "message": error}],
            "data": None,
        }

    # Success response
    return {
        "success": True,
        "message": "Successfully updated user",
        "errors": [],
        "data": user_data,
    }
