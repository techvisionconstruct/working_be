from typing import Optional, Tuple
from apps.contract.models import Contract
from apps.user.models import User


def get_contract_by_id_service(
    contract_id: str, user: User
) -> Tuple[Optional[Contract], Optional[str]]:
    try:
        # Check if the contract exists
        try:
            contract = Contract.objects.get(id=contract_id)
        except Contract.DoesNotExist:
            return None, f"Contract with ID {contract_id} not found."

        if user != contract.owner and user != contract.created_by and not user.is_staff:
            return None, "You don't have permission to view this contract."

        return contract, None
    except Exception as e:
        return None, f"Error retrieving contract: {str(e)}"
