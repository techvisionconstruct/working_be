from ninja import Router
from apps.proposal.services import delete_proposal_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Proposals"])


@router.delete("/{proposal_id}", auth=AuthBearer())
def delete_proposal_api(request, proposal_id: str):
    user = request.auth
    success, error = delete_proposal_service(proposal_id, user)
    if not success:
        return 404, {"error": error}
    return 200, {"success": True, "message": "Proposal deleted successfully"}
