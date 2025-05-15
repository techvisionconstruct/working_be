from ninja import Router
from apps.contract.services import create_contract_service
from apps.contract.dto import ContractCreateRequest, ContractResponse
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Contracts"])


@router.post("/", auth=AuthBearer())
def create_contract_api(request, payload: ContractCreateRequest):

    contract, error = create_contract_service(payload, request.auth)

    if error:
        if "permission" in error.lower():
            formatted_error = "Failed to create contract. You don't have permission."
        elif "not found" in error.lower():
            formatted_error = f"Failed to create contract. {error}"
        else:
            formatted_error = f"Failed to create contract. {error}"
        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Contract created successfully",
        "data": ContractResponse.from_orm(contract),
    }
