from typing import Optional, Tuple
from datetime import datetime
from apps.contract.models import Contract
from apps.contract.dto import ContractCreateRequest

from apps.proposal.models import Proposal
from apps.user.models import User


def create_contract_service(
    payload: ContractCreateRequest, user: User
) -> Tuple[Optional[Contract], Optional[str]]:
    try:
        # Handle proposal if provided
        proposal = None
        if payload.proposal_id:
            try:
                proposal = Proposal.objects.get(id=payload.proposal_id)
            except Proposal.DoesNotExist:
                return None, f"Proposal with ID {payload.proposal_id} does not exist."

        print(payload.contractor_initials)
        # Create and save the contract
        contract = Contract(
            name=payload.name,
            description=payload.description,
            status=payload.status if payload.status else "draft",
            terms=payload.terms,
            contractor_initials=payload.contractor_initials,
            contractor_signature=payload.contractor_signature,
            owner=user,
            created_by=user,
            updated_by=user,
        )

        if payload.contractor_initials:
            contract.contractor_signed_at = datetime.now()

        contract.save()

        # Link the proposal to this contract if a proposal was provided
        if proposal:
            proposal.contract = contract
            proposal.save()

        return contract, None
    except Exception as e:
        return None, f"Error creating contract: {str(e)}"
