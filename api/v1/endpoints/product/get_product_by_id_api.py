from ninja import Router, Path

from apps.product.dto import ProductDetailResponse
from apps.product.services import get_product_by_id_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Products"])


@router.get("/{product_id}/", response=ProductDetailResponse, auth=AuthBearer())
def get_product_by_id_api(
    request, product_id: str = Path(..., description="Product ID")
):
    product, error = get_product_by_id_service(product_id, request.auth)

    if error:
        if "not found" in error.lower():
            formatted_error = f"Failed to retrieve product. Product not found."
        elif "permission" in error.lower():
            formatted_error = f"Failed to access product. You don't have permission."
        else:
            formatted_error = f"Failed to retrieve product. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully retrieved product",
        "data": product,
    }
