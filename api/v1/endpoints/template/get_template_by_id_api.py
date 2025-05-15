from ninja import Router, Path

from apps.template.dto import TemplateDetailResponse
from apps.template.services import get_template_by_id_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Templates"])


@router.get("/{template_id}/", response=TemplateDetailResponse, auth=AuthBearer())
def get_template_by_id_api(
    request, template_id: str = Path(..., description="Template ID")
):
    template, error = get_template_by_id_service(template_id, request.auth)

    if error:
        if "not found" in error.lower():
            formatted_error = f"Failed to retrieve template. Template not found."
        elif "permission" in error.lower():
            formatted_error = f"Failed to access template. You don't have permission."
        else:
            formatted_error = f"Failed to retrieve template. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully retrieved template",
        "data": template,
    }
