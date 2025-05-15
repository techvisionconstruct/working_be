from typing import Optional, Tuple

from apps.variable_type.models import VariableType
from apps.user.models import User


def get_variable_type_by_id_service(
    variable_type_id: str, user: User
) -> Tuple[Optional[VariableType], Optional[str]]:
    try:
        # Try to find the variable_type
        variable_type = VariableType.objects.filter(id=variable_type_id).first()

        # If variable_type doesn't exist
        if not variable_type:
            return None, "VariableType not found"

        # Check if user has access (user is owner or variable_type is public)
        if variable_type.created_by != user and not variable_type.is_built_in:
            return None, "You don't have permission to access this variable_type"

        return variable_type, None
    except Exception as e:
        return None, f"Error retrieving variableType: {str(e)}"
