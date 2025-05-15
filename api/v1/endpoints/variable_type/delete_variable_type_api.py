# filepath: /Users/naigggs/Documents/Projects/service/api/v1/endpoints/variable_type/delete_variable_type_api.py
from ninja import Router, Path

from apps.variable_type.services import delete_variable_type_service
from apps.auth.services.authenticate_service import AuthBearer


router = Router(tags=["Variable Types"])


@router.delete("/{variable_type_id}/", auth=AuthBearer())
def delete_variable_type_api(
    request, variable_type_id: str = Path(..., description="Variable Type ID")
):
    success, error = delete_variable_type_service(variable_type_id, request.auth)

    if not success:
        if "not found" in error.lower():
            formatted_error = "Failed to delete variable type. Variable type not found."
        elif "built-in" in error.lower():
            formatted_error = (
                "Failed to delete variable type. Cannot delete built-in variable types."
            )
        elif "permission" in error.lower():
            formatted_error = (
                "Failed to delete variable type. You don't have permission."
            )
        else:
            formatted_error = f"Failed to delete variable type. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully deleted variable type",
        "data": None,
    }
