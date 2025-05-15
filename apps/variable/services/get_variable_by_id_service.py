# filepath: /Users/naigggs/Documents/Projects/service/apps/variable/services/get_variable_by_id_service.py
# filepath: /Users/naigggs/Documents/Projects/service/apps/variable/services/get_variable_by_id_service.py
from typing import Optional, Tuple

from apps.variable.models import Variable
from apps.user.models import User


def get_variable_by_id_service(
    variable_id: str, user: User
) -> Tuple[Optional[Variable], Optional[str]]:
    try:
        # Try to find the variable
        variable = Variable.objects.filter(id=variable_id).first()

        # If variable doesn't exist
        if not variable:
            return None, "Variable not found"

        # Check if user has access (user is owner or variable is global)
        if variable.created_by != user and not variable.is_global:
            return None, "You don't have permission to access this variable"

        return variable, None
    except Exception as e:
        return None, f"Error retrieving variable: {str(e)}"
