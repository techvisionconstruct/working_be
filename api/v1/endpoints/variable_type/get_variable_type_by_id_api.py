from ninja import Router, Path

from apps.variable_type.dto import VariableTypeDetailResponse
from apps.variable_type.services import get_variable_type_by_id_service
from apps.auth.services.authenticate_service import AuthBearer


router = Router(tags=["Variable Types"])


@router.get(
    "/{variable_type_id}/", response=VariableTypeDetailResponse, auth=AuthBearer()
)
def get_variable_type_by_id_api(
    request, variable_type_id: str = Path(..., description="Variable Type ID")
):
    variable_type, error = get_variable_type_by_id_service(
        variable_type_id, request.auth
    )

    if error:
        if "not found" in error.lower():
            formatted_error = (
                f"Failed to retrieve variable type. Variable type not found."
            )
        elif "permission" in error.lower():
            formatted_error = (
                f"Failed to access variable type. You don't have permission."
            )
        else:
            formatted_error = f"Failed to retrieve variable type. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully retrieved variable type",
        "data": variable_type,
    }
