from ninja import Router, Path

from apps.element.dto import ElementDetailResponse
from apps.element.services.get_element_by_id_service import get_element_by_id_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Elements"])


@router.get("/{element_id}/", response=ElementDetailResponse, auth=AuthBearer())
def get_element_by_id_api(
    request, element_id: str = Path(..., description="Element ID")
):
    element, error = get_element_by_id_service(element_id, request.auth)

    if error:
        if "not found" in error.lower():
            formatted_error = f"Failed to retrieve element. Element not found."
        elif "permission" in error.lower():
            formatted_error = f"Failed to access element. You don't have permission."
        else:
            formatted_error = f"Failed to retrieve element. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully retrieved element",
        "data": element,
    }
