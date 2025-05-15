from ninja import Router, Path

from apps.variable.dto import VariableDetailResponse
from apps.variable.services import get_variable_by_id_service
from apps.auth.services.authenticate_service import AuthBearer


router = Router(tags=["Variables"])


@router.get("/{variable_id}/", response=VariableDetailResponse, auth=AuthBearer())
def get_variable_by_id_api(
    request, variable_id: str = Path(..., description="Variable ID")
):
    variable, error = get_variable_by_id_service(variable_id, request.auth)

    if error:
        if "not found" in error.lower():
            formatted_error = f"Failed to retrieve variable. Variable not found."
        elif "permission" in error.lower():
            formatted_error = f"Failed to access variable. You don't have permission."
        else:
            formatted_error = f"Failed to retrieve variable. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully retrieved variable",
        "data": variable,
    }
