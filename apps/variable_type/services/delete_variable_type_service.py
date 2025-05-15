# filepath: /Users/naigggs/Documents/Projects/service/apps/variable_type/services/delete_variable_type_service.py
from typing import Optional, Tuple

from apps.variable_type.models import VariableType
from apps.user.models import User


def delete_variable_type_service(
    variable_type_id: str, user: User
) -> Tuple[bool, Optional[str]]:
    try:
        # Check if the variable type exists
        variable_type = VariableType.objects.filter(id=variable_type_id).first()
        if not variable_type:
            return False, f"Variable type with ID {variable_type_id} not found."

        # Check if it's a built-in variable type
        if variable_type.is_built_in:
            return False, "Cannot delete built-in variable types."

        # Check if user has permission (only delete their own non-built-in types)
        if variable_type.created_by != user and not variable_type.is_built_in:
            return False, "You do not have permission to delete this variable type."

        # Record the user who performed the deletion
        variable_type.updated_by = user

        # Delete the variable type
        variable_type.delete()

        return True, None
    except Exception as e:
        return False, f"Error deleting variable type: {str(e)}"
