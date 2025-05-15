from ninja import Router

from apps.variable.dto import VariableCreateRequest, VariableResponse
from apps.variable.services import create_variable_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Variables"])


@router.post("/", auth=AuthBearer())
def create_variable_api(request, payload: VariableCreateRequest):
    print(payload)
    variable, error = create_variable_service(payload, request.auth)

    if error:
        if "permission" in error.lower():
            formatted_error = "Failed to create variable. You don't have permission."
        elif "not found" in error.lower():
            formatted_error = f"Failed to create variable. {error}"
        else:
            formatted_error = f"Failed to create variable. {error}"
        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully created variable",
        "data": VariableResponse.from_orm(variable),
    }
