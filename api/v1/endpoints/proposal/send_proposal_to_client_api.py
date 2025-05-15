from ninja import Router
from apps.proposal.services.send_proposal_to_client_service import (
    send_proposal_to_client_service,
)
from ninja.errors import HttpError
from apps.proposal.dto import SendProposalRequest

router = Router(tags=["Proposals"])





@router.post("/", response={200: dict, 400: dict})
def send_proposal_to_client_api(request, data: SendProposalRequest):
    success, error = send_proposal_to_client_service(
        data
    )
    if not success:
        return 400, {"error": error}
    return 200, {"message": "Proposal sent successfully"}
