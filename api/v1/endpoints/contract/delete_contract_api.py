from ninja import Router
from apps.contract.services import delete_contract_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Contracts"])


@router.delete("/{contract_id}/", auth=AuthBearer())
def delete_contract_api(request, contract_id: str):
    user = request.auth
    success, error = delete_contract_service(contract_id, user)

    if not success:
        if "not found" in error.lower():
            return 404, {"success": False, "message": f"Contract not found."}
        elif "permission" in error.lower():
            return 403, {
                "success": False,
                "message": "You don't have permission to delete this contract.",
            }
        else:
            return 400, {"success": False, "message": error}

    return 200, {"success": True, "message": "Contract deleted successfully"}
