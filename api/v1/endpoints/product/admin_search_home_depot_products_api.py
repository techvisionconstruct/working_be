from ninja import Router
from django.http import HttpRequest
from ninja.responses import Response

from apps.product.dto import ProductSearchRequest, HomeDepotProductSearchResponse
from apps.product.services.admin.home_depot import (
    admin_search_home_depot_products_service,
)
from apps.auth.services.authenticate_service import AuthBearer
from apps.user.choices import UserRole

router = Router(tags=["Products"])


@router.post(
    "/",
    response={
        200: HomeDepotProductSearchResponse,
        403: HomeDepotProductSearchResponse,
    },
    auth=AuthBearer(),
)
def admin_search_home_depot_products_api(
    request: HttpRequest, payload: ProductSearchRequest
):
    # Check if user is authenticated and has admin privileges
    if not request.auth or request.auth.role != UserRole.ADMIN:
        # Build base URL for pagination links
        base_url = f"{request.build_absolute_uri(request.path)}?"

        return Response(
            {
                "success": False,
                "message": "Failed to search products. Insufficient permissions.",
                "data": [],
                "links": {
                    "self": f"{base_url}page=1&page_size=0",
                    "first": f"{base_url}page=1&page_size=0",
                    "last": f"{base_url}page=1&page_size=0",
                },
                "meta": {
                    "current_page": 1,
                    "total_pages": 0,
                    "page_size": 0,
                    "total_count": 0,
                },
            },
            status=403,
        )

    # Call service to search products
    products, error = admin_search_home_depot_products_service(
        payload.search_term, payload.sort_by, request.auth
    )

    if error:
        # Build base URL for pagination links
        base_url = f"{request.build_absolute_uri(request.path)}?"

        return {
            "success": False,
            "message": f"Failed to search products. {error}",
            "data": [],
            "links": {
                "self": f"{base_url}page=1&page_size=0",
                "first": f"{base_url}page=1&page_size=0",
                "last": f"{base_url}page=1&page_size=0",
            },
            "meta": {
                "current_page": 1,
                "total_pages": 0,
                "page_size": 0,
                "total_count": 0,
            },
        }

    # Build base URL for pagination links
    base_url = f"{request.build_absolute_uri(request.path)}?"

    # For search results, we're returning all at once, so we use a single page
    current_page = 1
    total_pages = 1
    page_size = len(products)

    return {
        "success": True,
        "message": f"Successfully searched products. Found {len(products)} products",
        "data": products,
        "links": {
            "self": f"{base_url}page={current_page}&page_size={page_size}",
            "first": f"{base_url}page=1&page_size={page_size}",
            "last": f"{base_url}page={total_pages}&page_size={page_size}",
        },
        "meta": {
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": page_size,
            "total_count": len(products),
        },
    }
