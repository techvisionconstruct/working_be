from ninja import Router, Path

from apps.template.services.delete_template_service import delete_template_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Templates"])


@router.delete("/{template_id}/", auth=AuthBearer())
def delete_template_api(
    request, template_id: str = Path(..., description="Template ID")
):
    success, error = delete_template_service(template_id, request.auth)

    if not success:
        if "not found" in error.lower():
            formatted_error = "Failed to delete template. Template not found."
        elif "permission" in error.lower():
            formatted_error = "Failed to delete template. You don't have permission."
        elif "source for derived templates" in error.lower():
            formatted_error = "Failed to delete template. It is used as a source for derived templates."
        else:
            formatted_error = f"Failed to delete template. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully deleted template",
        "data": None,
    }
