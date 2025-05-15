from typing import Optional
from ninja import Router, Query

from apps.contract.dto import ContractListResponse
from apps.contract.services import get_all_contracts_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Contracts"])


@router.get("/", response=ContractListResponse, auth=AuthBearer())
def get_all_contracts_api(
    request,
    search: Optional[str] = Query(None, description="Search term"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Items per page"),
):
    # Get contracts and pagination info from service
    contracts, pagination_info = get_all_contracts_service(
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
        "message": "Contracts retrieved successfully",
        "data": contracts,
        "links": links,
        "meta": pagination_info,
    }
