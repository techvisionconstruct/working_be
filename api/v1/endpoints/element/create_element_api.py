from ninja import Router

from apps.element.dto import ElementCreateRequest, ElementResponse
from apps.element.services.create_element_service import create_element_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Elements"])


@router.post("/", auth=AuthBearer())
def create_element_api(request, payload: ElementCreateRequest):
    element, error = create_element_service(payload, request.auth)

    if error:
        if "permission" in error.lower():
            formatted_error = "Failed to create element. You don't have permission."
        else:
            formatted_error = f"Failed to create element. {error}"
        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully created element",
        "data": ElementResponse.from_orm(element),
    }
