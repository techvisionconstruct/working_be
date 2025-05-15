from typing import Optional
from ninja import Router, Query
from django.http import HttpRequest

from apps.user.dto import AdminUserListResponse
from apps.user.services.admin import admin_get_all_users_service
from apps.user.choices import UserRole
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["User Management"])


@router.get("/", response=AdminUserListResponse, auth=AuthBearer())
def admin_get_all_users_api(
    request: HttpRequest,
    search: Optional[str] = Query(
        None, description="Search term for name, email or username"
    ),
    role: Optional[str] = Query(None, description="Filter by user role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_staff: Optional[bool] = Query(None, description="Filter by staff status"),
    is_superuser: Optional[bool] = Query(
        None, description="Filter by superuser status"
    ),
    page: int = Query(1, description="Page number", gt=0),
    page_size: int = Query(10, description="Items per page", ge=1, le=100),
    sort_by: str = Query(
        "-created_at", description="Field to sort by (prefix with - for descending)"
    ),
):
    # Check admin privileges
    if not request.auth or request.auth.role != UserRole.ADMIN:
        return {
            "success": False,
            "message": "Failed to retrieve users. Insufficient permissions.",
            "errors": [
                {
                    "field": "general",
                    "message": "Only administrators can view all users",
                }
            ],
            "data": [],
            "links": {
                "self": request.build_absolute_uri(request.path)
                + "?page=1&page_size=10",
                "first": request.build_absolute_uri(request.path)
                + "?page=1&page_size=10",
                "last": request.build_absolute_uri(request.path)
                + "?page=1&page_size=10",
                "next": None,
                "prev": None,
            },
            "meta": {
                "current_page": 1,
                "total_pages": 0,
                "page_size": page_size,
                "total_count": 0,
            },
        }

    # Get users and pagination info from service
    users, pagination_info = admin_get_all_users_service(
        admin_user=request.auth,
        search=search,
        role=role,
        is_active=is_active,
        is_staff=is_staff,
        is_superuser=is_superuser,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
    )

    # Build base URL for pagination links
    base_url = f"{request.build_absolute_uri(request.path)}?"
    if search:
        base_url += f"search={search}&"
    if role:
        base_url += f"role={role}&"
    if is_active is not None:
        base_url += f"is_active={str(is_active).lower()}&"
    if is_staff is not None:
        base_url += f"is_staff={str(is_staff).lower()}&"
    if is_superuser is not None:
        base_url += f"is_superuser={str(is_superuser).lower()}&"
    if sort_by and sort_by != "-created_at":
        base_url += f"sort_by={sort_by}&"

    # Generate HATEOAS links
    current_page = pagination_info["current_page"]
    total_pages = pagination_info["total_pages"]

    links = {
        "self": f"{base_url}page={current_page}&page_size={page_size}",
        "first": f"{base_url}page=1&page_size={page_size}",
        "last": (
            f"{base_url}page={total_pages}&page_size={page_size}"
            if total_pages > 0
            else f"{base_url}page=1&page_size={page_size}"
        ),
        "next": (
            f"{base_url}page={current_page + 1}&page_size={page_size}"
            if current_page < total_pages
            else None
        ),
        "prev": (
            f"{base_url}page={current_page - 1}&page_size={page_size}"
            if current_page > 1
            else None
        ),
    }

    return {
        "success": True,
        "message": f"Successfully retrieved users. Found {pagination_info['total_count']} users",
        "data": users,
        "links": links,
        "meta": pagination_info,
    }
