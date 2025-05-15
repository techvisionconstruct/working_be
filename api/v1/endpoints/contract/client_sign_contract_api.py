from ninja import Router, Path
from apps.contract.services import client_sign_contract_service
from apps.contract.dto import ContractSignRequest, ContractResponse
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Contracts"])


@router.patch("/{contract_id}/")
def client_sign_contract_api(
    request,
    payload: ContractSignRequest,
    contract_id: str = Path(..., description="Contract ID"),
):
    contract, error = client_sign_contract_service(contract_id, payload, None)

    if error:
        if "not found" in error.lower():
            formatted_error = "Failed to sign contract. Contract not found."
        elif "signature" in error.lower():
            formatted_error = error
        else:
            formatted_error = f"Failed to sign contract. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Contract successfully signed by client",
        "data": ContractResponse.from_orm(contract),
    }
