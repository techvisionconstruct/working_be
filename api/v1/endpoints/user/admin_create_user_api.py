from ninja import Router, Path
from django.http import HttpRequest
from ninja.responses import Response

from apps.user.dto import AdminCreateUserRequest, AdminCreateUserResponse
from apps.user.services.admin import admin_create_user_service
from apps.user.choices import UserRole
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["User Management"])


@router.post(
    "/",
    response={
        201: AdminCreateUserResponse,
        400: AdminCreateUserResponse,
        403: AdminCreateUserResponse,
    },
    auth=AuthBearer(),
)
def admin_create_user_api(request: HttpRequest, payload: AdminCreateUserRequest):
    # Check if user is authenticated and has admin privileges
    if not request.auth or request.auth.role != UserRole.ADMIN:
        return Response(
            {
                "success": False,
                "message": "Failed to create user. Insufficient permissions.",
                "errors": [
                    {
                        "field": "general",
                        "message": "Only administrators can create users",
                    }
                ],
                "user": None,
            },
            status=403,
        )

    # Call service to create user
    user_data, error = admin_create_user_service(
        admin_user=request.auth,
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name,
        last_name=payload.last_name,
        username=payload.username,
        role=payload.role,
        is_active=payload.is_active,
        is_staff=payload.is_staff,
        is_superuser=payload.is_superuser,
    )

    # Handle error response
    if error:
        # Map errors to specific fields
        field_errors = []

        if "Email already registered" in error:
            field_errors.append(
                {"field": "email", "message": "Email already registered"}
            )
            formatted_error = "Failed to create user. Email already registered."
        elif "Permission denied" in error:
            field_errors.append(
                {"field": "general", "message": "Insufficient permissions"}
            )
            formatted_error = "Failed to create user. Insufficient permissions."
        else:
            field_errors.append({"field": "general", "message": error})
            formatted_error = f"Failed to create user. {error}"

        status_code = (
            400 if "Email already" in error else 403 if "Permission" in error else 400
        )

        return Response(
            {
                "success": False,
                "message": formatted_error,
                "errors": field_errors,
                "user": None,
            },
            status=status_code,
        )

    # Success response
    return Response(
        {
            "success": True,
            "message": "Successfully created user",
            "errors": [],
            "user": user_data,
        },
        status=201,
    )
