from ninja import Router, Path

from apps.element.services.delete_element_service import delete_element_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Elements"])


@router.delete("/{element_id}/", auth=AuthBearer())
def delete_element_api(request, element_id: str = Path(..., description="Element ID")):
    success, error = delete_element_service(element_id, request.auth)

    if not success:
        if "not found" in error.lower():
            formatted_error = "Failed to delete element. Element not found."
        elif "permission" in error.lower():
            formatted_error = "Failed to delete element. You don't have permission."
        else:
            formatted_error = f"Failed to delete element. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully deleted element",
        "data": None,
    }
