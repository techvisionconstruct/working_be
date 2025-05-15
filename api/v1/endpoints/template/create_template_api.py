from ninja import Router

from apps.template.dto import TemplateCreateRequest, TemplateResponse
from apps.template.services.create_template_service import create_template_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Templates"])


@router.post("/", auth=AuthBearer())
def create_template_api(request, payload: TemplateCreateRequest):

    template, error = create_template_service(payload, request.auth)

    if error:
        if "permission" in error.lower():
            formatted_error = "Failed to create template. You don't have permission."
        elif "not found" in error.lower():
            formatted_error = f"Failed to create template. {error}"
        else:
            formatted_error = f"Failed to create template. {error}"
        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully created template",
        "data": TemplateResponse.from_orm(template),
    }
