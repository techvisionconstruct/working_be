from ninja import Router, Path
from apps.proposal.services import update_proposal_service
from apps.proposal.dto import ProposalUpdateRequest, ProposalResponse
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Proposals"])


@router.put("/{proposal_id}/", auth=AuthBearer())
def update_proposal_api(
    request,
    payload: ProposalUpdateRequest,
    proposal_id: str = Path(..., description="Proposal ID"),
):
    proposal, error = update_proposal_service(
        proposal_id, payload.dict(exclude_unset=True), request.auth
    )
    if error:
        if "not found" in error.lower():
            formatted_error = "Failed to update proposal. Proposal not found."
        elif "permission" in error.lower():
            formatted_error = "Failed to update proposal. You don't have permission."
        else:
            formatted_error = f"Failed to update proposal. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Proposal updated successfully",
        "data": ProposalResponse.from_orm(proposal),
    }
