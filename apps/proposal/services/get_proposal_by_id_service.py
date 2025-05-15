from typing import Optional, Tuple
from apps.proposal.models import Proposal
from apps.user.models import User


def get_proposal_by_id_service(
    proposal_id: str, user: User
) -> Tuple[Optional[Proposal], Optional[str]]:
    try:
        proposal = Proposal.objects.filter(id=proposal_id).first()
        if not proposal:
            return None, "Proposal not found"

        if proposal.created_by != user:
            return None, "You don't have permission to access this proposal"
        return proposal, None
    except Exception as e:
        return None, f"Error retrieving proposal: {str(e)}"
