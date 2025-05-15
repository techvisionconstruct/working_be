from ninja import Router, Path

from apps.template.dto import TemplateResponse, TemplateUpdateRequest
from apps.template.services.update_template_service import update_template_service
from apps.auth.services.authenticate_service import AuthBearer


router = Router(tags=["Templates"])


@router.put("/{template_id}/", auth=AuthBearer())
def update_template_api(
    request,
    payload: TemplateUpdateRequest,
    template_id: str = Path(..., description="Template ID"),
):
    template, error = update_template_service(
        template_id, payload.dict(exclude_unset=True), request.auth
    )

    if error:
        if "not found" in error.lower():
            formatted_error = "Failed to update template. Template not found."
        elif "permission" in error.lower():
            formatted_error = "Failed to update template. You don't have permission."
        else:
            formatted_error = f"Failed to update template. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully updated template",
        "data": TemplateResponse.from_orm(template),
    }
