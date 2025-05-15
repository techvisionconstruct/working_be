from typing import Optional, Tuple
from datetime import datetime
from apps.contract.models import Contract
from apps.contract.dto import ContractSignRequest
from apps.user.models import User
from helpers.process_base64_image import process_base64_image


def client_sign_contract_service(
    contract_id: str, payload: ContractSignRequest, user=User
) -> Tuple[Optional[Contract], Optional[str]]:
    try:
        # Check if the contract exists
        print(payload)
        try:
            contract = Contract.objects.get(id=contract_id)
        except Contract.DoesNotExist:
            return None, f"Contract with ID {contract_id} not found."

        # Track if any signature was added or updated
        signature_updated = False
        current_time = datetime.now()

        # Process client signature
        if payload.client_signature:
            try:
                client_signature_file = process_base64_image(payload.client_signature)
                contract.client_signature = client_signature_file
                contract.client_signed_at = current_time
                signature_updated = True
            except Exception as e:
                return None, f"Error processing client signature: {str(e)}"

        # Process client initials
        if payload.client_initials:
            contract.client_initials = payload.client_initials
            contract.client_signed_at = current_time
            signature_updated = True

        # Update contract status if both signatures are present
        if (
            contract.client_signed_at
            and contract.contractor_signed_at
            and contract.status != "signed"
        ):
            contract.status = "signed"

        # Only save if there were actual changes
        if signature_updated:
            # Update the 'updated_by' field
            contract.updated_by = user if user else None
            contract.save()
            return contract, None
        else:
            return None, "No client signature data provided."

    except Exception as e:
        return None, f"Error signing contract: {str(e)}"
