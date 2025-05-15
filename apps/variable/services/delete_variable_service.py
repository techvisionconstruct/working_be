# filepath: /Users/naigggs/Documents/Projects/service/apps/variable/services/delete_variable_service.py
# filepath: /Users/naigggs/Documents/Projects/service/apps/variable/services/delete_variable_service.py
from typing import Optional, Tuple

from apps.variable.models import Variable
from apps.user.models import User


def delete_variable_service(variable_id: str, user: User) -> Tuple[bool, Optional[str]]:
    try:
        # Check if the variable exists
        try:
            variable = Variable.objects.get(id=variable_id)
        except Variable.DoesNotExist:
            return False, f"Variable with ID {variable_id} not found."

        # Check permissions
        if variable.created_by != user and not user.is_staff:
            return False, "You do not have permission to delete this variable."

        # Record the user who performed the deletion
        variable.updated_by = user

        # Delete the variable
        variable.delete()

        return True, None
    except Exception as e:
        return False, f"Error deleting variable: {str(e)}"
