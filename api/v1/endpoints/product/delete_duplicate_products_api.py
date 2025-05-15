from ninja import Router
from ninja.responses import Response

from apps.auth.services.authenticate_service import AuthBearer
from apps.product.services import delete_duplicate_products_service

router = Router(tags=["Products"])


@router.delete("/", auth=AuthBearer())
def delete_duplicate_products_api(request):
    user = request.auth
    deleted_count, error = delete_duplicate_products_service(user)

    if error and "No duplicate products found" not in error:
        return Response(
            {"success": False, "message": error, "deleted_count": 0}, status=500
        )

    if "No duplicate products found" in str(error):
        return Response(
            {
                "success": True,
                "message": "No duplicate products found to delete.",
                "deleted_count": 0,
            },
            status=200,
        )

    return Response(
        {
            "success": True,
            "message": f"Successfully deleted {deleted_count} duplicate product(s).",
            "deleted_count": deleted_count,
        },
        status=200,
    )
