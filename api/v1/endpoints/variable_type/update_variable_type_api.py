from ninja import Router, Path

from apps.variable_type.dto import VariableTypeUpdateRequest, VariableTypeResponse
from apps.variable_type.services import update_variable_type_service
from apps.auth.services.authenticate_service import AuthBearer


router = Router(tags=["Variable Types"])


@router.put("/{variable_type_id}/", auth=AuthBearer())
def update_variable_type_api(
    request,
    payload: VariableTypeUpdateRequest,
    variable_type_id: str = Path(..., description="Variable Type ID"),
):
    variable_type, error = update_variable_type_service(
        variable_type_id, payload, request.auth
    )

    if error:
        if "not found" in error.lower():
            formatted_error = "Failed to update variable type. Variable type not found."
        elif "built-in" in error.lower():
            formatted_error = (
                "Failed to update variable type. Cannot modify built-in variable types."
            )
        elif "permission" in error.lower():
            formatted_error = (
                "Failed to update variable type. You don't have permission."
            )
        else:
            formatted_error = f"Failed to update variable type. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully updated variable type",
        "data": VariableTypeResponse.from_orm(variable_type),
    }
