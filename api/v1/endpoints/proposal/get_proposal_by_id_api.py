from ninja import Router, Path

from apps.proposal.dto import ProposalDetailResponse
from apps.proposal.services.get_proposal_by_id_service import get_proposal_by_id_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Proposals"])


@router.get("/{proposal_id}/", response=ProposalDetailResponse, auth=AuthBearer())
def get_proposal_by_id_api(
    request, proposal_id: str = Path(..., description="Proposal ID")
):
    proposal, error = get_proposal_by_id_service(proposal_id, request.auth)

    if error:
        if "not found" in error.lower():
            formatted_error = f"Failed to retrieve proposal. Proposal not found."
        elif "permission" in error.lower():
            formatted_error = f"Failed to access proposal. You don't have permission."
        else:
            formatted_error = f"Failed to retrieve proposal. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully retrieved proposal",
        "data": proposal,
    }
