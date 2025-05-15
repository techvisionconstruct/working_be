from ninja import Router, Path

from apps.contract.dto import ContractDetailResponse
from apps.contract.services import get_contract_by_id_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Contracts"])


@router.get("/{contract_id}/", response=ContractDetailResponse, auth=AuthBearer())
def get_contract_by_id_api(
    request, contract_id: str = Path(..., description="Contract ID")
):
    contract, error = get_contract_by_id_service(contract_id, request.auth)

    if error:
        if "not found" in error.lower():
            formatted_error = "Failed to retrieve contract. Contract not found."
        elif "permission" in error.lower():
            formatted_error = "Failed to access contract. You don't have permission."
        else:
            formatted_error = f"Failed to retrieve contract. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully retrieved contract",
        "data": contract,
    }
