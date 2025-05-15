# filepath: /Users/naigggs/Documents/Projects/service/api/v1/endpoints/variable_type/post_variable_type_api.py
from ninja import Router, Path

from apps.variable_type.dto import VariableTypeCreateRequest, VariableTypeResponse
from apps.variable_type.services import post_variable_type_service
from api.v1.endpoints.auth.authenticate import AuthBearer

router = Router(tags=["Variable Types"])


@router.post("/", auth=AuthBearer())
def post_variable_type_api(request, payload: VariableTypeCreateRequest):
    variable_type, error = post_variable_type_service(payload, request.auth)

    if error:
        if "permission" in error.lower():
            formatted_error = (
                f"Failed to create variable type. You don't have permission."
            )
        else:
            formatted_error = f"Failed to create variable type. {error}"
        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully created variable type",
        "data": VariableTypeResponse.from_orm(variable_type),
    }
