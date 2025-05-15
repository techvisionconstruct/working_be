from typing import Optional, Tuple
from apps.proposal.models import Proposal
from apps.user.models import User


def delete_proposal_service(proposal_id: str, user: User) -> Tuple[bool, Optional[str]]:
    try:
        proposal = Proposal.objects.filter(id=proposal_id, owner=user).first()
        if not proposal:
            return (
                False,
                "Proposal not found or you do not have permission to delete it.",
            )
        proposal.delete()
        return True, None
    except Exception as e:
        return False, f"Error deleting proposal: {str(e)}"
