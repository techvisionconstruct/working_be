from ninja import Router, Path

from apps.variable.services import delete_variable_service
from apps.auth.services.authenticate_service import AuthBearer


router = Router(tags=["Variables"])


@router.delete("/{variable_id}/", auth=AuthBearer())
def delete_variable_api(
    request, variable_id: str = Path(..., description="Variable ID")
):
    success, error = delete_variable_service(variable_id, request.auth)

    if not success:
        if "not found" in error.lower():
            formatted_error = "Failed to delete variable. Variable not found."
        elif "permission" in error.lower():
            formatted_error = "Failed to delete variable. You don't have permission."
        else:
            formatted_error = f"Failed to delete variable. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully deleted variable",
        "data": None,
    }
