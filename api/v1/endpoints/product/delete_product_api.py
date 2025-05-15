from ninja import Router, Path

from apps.product.services import delete_product_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Products"])


@router.delete("/{product_id}/", auth=AuthBearer())
def delete_product_api(request, product_id: str = Path(..., description="Product ID")):
    success, error = delete_product_service(product_id, request.auth)

    if not success:
        if "not found" in error.lower():
            formatted_error = "Failed to delete product. Product not found."
        elif "permission" in error.lower():
            formatted_error = "Failed to delete product. You don't have permission."
        else:
            formatted_error = f"Failed to delete product. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully deleted product",
        "data": None,
    }
