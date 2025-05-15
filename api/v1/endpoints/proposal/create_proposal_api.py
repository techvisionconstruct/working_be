from ninja import Router
from apps.proposal.services import create_proposal_service
from apps.proposal.dto import ProposalCreateRequest, ProposalResponse
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Proposals"])


@router.post("/", auth=AuthBearer())
def create_proposal_api(request, payload: ProposalCreateRequest):

    proposal, error = create_proposal_service(payload, request.auth)

    if error:
        if "permission" in error.lower():
            formatted_error = "Failed to create proposal. You don't have permission."
        elif "not found" in error.lower():
            formatted_error = f"Failed to create proposal. {error}"
        else:
            formatted_error = f"Failed to create proposal. {error}"
        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Proposal created successfully",
        "data": ProposalResponse.from_orm(proposal),
    }
