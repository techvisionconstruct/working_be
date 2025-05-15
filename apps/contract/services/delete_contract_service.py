from typing import Optional, Tuple
from apps.contract.models import Contract
from apps.user.models import User


def delete_contract_service(contract_id: str, user: User) -> Tuple[bool, Optional[str]]:
    try:
        # Check if the contract exists
        try:
            contract = Contract.objects.get(id=contract_id)
        except Contract.DoesNotExist:
            return False, f"Contract with ID {contract_id} not found."

        # Check if user has permission to delete this contract
        # Only allow the creator or staff members to delete a contract
        if contract.created_by != user and not user.is_staff:
            return False, "You don't have permission to delete this contract."

        # Delete the contract
        # This will also delete related objects due to cascade delete settings
        contract.delete()

        return True, None
    except Exception as e:
        return False, f"Error deleting contract: {str(e)}"
