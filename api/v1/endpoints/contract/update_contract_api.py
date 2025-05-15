from ninja import Router, Path
from apps.contract.services import update_contract_service
from apps.contract.dto import ContractUpdateRequest, ContractResponse
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Contracts"])


@router.put("/{contract_id}/", auth=AuthBearer())
def update_contract_api(
    request,
    payload: ContractUpdateRequest,
    contract_id: str = Path(..., description="Contract ID"),
):
    contract, error = update_contract_service(
        contract_id, payload.dict(exclude_unset=True), request.auth
    )

    if error:
        if "not found" in error.lower():
            formatted_error = "Failed to update contract. Contract not found."
        elif "permission" in error.lower():
            formatted_error = "Failed to update contract. You don't have permission."
        else:
            formatted_error = f"Failed to update contract. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Contract updated successfully",
        "data": ContractResponse.from_orm(contract),
    }
