from typing import Optional
from ninja import Router, Query

from apps.variable.dto import VariableListResponse
from apps.variable.services import get_all_variable_service
from apps.auth.services.authenticate_service import AuthBearer


router = Router(tags=["Variables"])


@router.get("/", response=VariableListResponse, auth=AuthBearer())
def get_all_variable_api(
    request,
    search: Optional[str] = Query(None, description="Search term"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Items per page"),
):
    # Get variables and pagination info from service
    variables, pagination_info = get_all_variable_service(
        request.auth, search, page, page_size
    )

    # Build base URL for pagination links
    base_url = f"{request.build_absolute_uri(request.path)}?"
    if search:
        base_url += f"search={search}&"

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
        "message": f"Successfully retrieved variables. Found {pagination_info['total_count']} variables",
        "data": variables,
        "links": links,
        "meta": pagination_info,
    }
