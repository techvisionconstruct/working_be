from ninja import Router, Path

from apps.variable.dto import VariableUpdateRequest, VariableResponse
from apps.variable.services import update_variable_service
from apps.auth.services.authenticate_service import AuthBearer


router = Router(tags=["Variables"])


@router.put("/{variable_id}/", auth=AuthBearer())
def update_variable_api(
    request,
    payload: VariableUpdateRequest,
    variable_id: str = Path(..., description="Variable ID"),
):
    variable, error = update_variable_service(variable_id, payload, request.auth)

    if error:
        if "not found" in error.lower():
            formatted_error = "Failed to update variable. Variable not found."
        elif "permission" in error.lower():
            formatted_error = "Failed to update variable. You don't have permission."
        else:
            formatted_error = f"Failed to update variable. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully updated variable",
        "data": VariableResponse.from_orm(variable),
    }
