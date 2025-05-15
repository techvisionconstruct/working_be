from typing import Optional, Tuple
from apps.proposal.models import Proposal
from apps.contract.models import Contract
from apps.user.models import User


def get_client_proposal_by_id_service(
    proposal_id: str
) -> Tuple[Optional[Proposal], Optional[str]]:
    try:
        proposal = Proposal.objects.filter(id=proposal_id).first()
        # contract = Contract.objects.filter(id=proposal.contract_id).first()
        # print(contract)
        if not proposal:
            return None, "Proposal not found"

        return proposal, None
    except Exception as e:
        return None, f"Error retrieving proposal: {str(e)}"
