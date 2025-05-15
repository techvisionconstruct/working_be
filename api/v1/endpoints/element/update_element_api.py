from ninja import Router, Path

from apps.element.dto import ElementResponse, ElementUpdateRequest
from apps.element.services.update_element_service import update_element_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Elements"])


@router.put("/{element_id}/", auth=AuthBearer())
def update_element_api(
    request,
    element_id: str = Path(..., description="Element ID"),
    payload: ElementUpdateRequest = None,
):
    element, error = update_element_service(element_id, payload, request.auth)

    if error:
        if "not found" in error.lower():
            formatted_error = "Failed to update element. Element not found."
        elif "permission" in error.lower():
            formatted_error = "Failed to update element. You don't have permission."
        else:
            formatted_error = f"Failed to update element. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully updated element",
        "data": ElementResponse.from_orm(element),
    }
