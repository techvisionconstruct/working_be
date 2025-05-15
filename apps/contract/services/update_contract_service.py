from typing import Optional, Tuple
from datetime import datetime
from apps.contract.models import Contract
from apps.proposal.models import Proposal
from apps.user.models import User
from helpers.process_base64_image import process_base64_image


def update_contract_service(
    contract_id: str,
    payload: dict,
    user: User,
) -> Tuple[Optional[Contract], Optional[str]]:
    try:
        # Check if the contract exists
        print(payload)
        try:
            contract = Contract.objects.get(id=contract_id)
        except Contract.DoesNotExist:
            return None, f"Contract with ID {contract_id} not found."

        # Check if user has permission
        if contract.created_by != user and not user.is_staff:
            return None, "You don't have permission to update this contract."

        # Update fields if provided in payload
        if "name" in payload:
            contract.name = payload["name"]

        if "description" in payload:
            contract.description = payload["description"]

        if "status" in payload:
            contract.status = payload["status"]

        if "terms" in payload:
            contract.terms = payload["terms"]

        if "contractor_initials" in payload:
            contract.contractor_initials = payload["contractor_initials"]
            contract.contractor_signed_at = datetime.now()

        if "contractor_signature" in payload:
            try:
                contractor_signature_file = process_base64_image(
                    payload["contractor_signature"]
                )
                contract.contractor_signature = contractor_signature_file
                contract.contractor_signed_at = datetime.now()
            except Exception as e:
                return None, f"Error processing contractor signature: {str(e)}"

        # Update the 'updated_by' field
        contract.updated_by = user

        contract.save()
        return contract, None
    except Exception as e:
        return None, f"Error updating contract: {str(e)}"
