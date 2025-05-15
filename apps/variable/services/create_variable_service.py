# filepath: /Users/naigggs/Documents/Projects/service/apps/variable/services/post_variable_service.py
# filepath: /Users/naigggs/Documents/Projects/service/apps/variable/services/post_variable_service.py
from typing import Optional, Tuple

from apps.variable.models import Variable
from apps.user.models import User
from apps.variable.dto import VariableCreateRequest
from apps.variable_type.models import VariableType


def create_variable_service(
    payload: VariableCreateRequest, user: User
) -> Tuple[Optional[Variable], Optional[str]]:
    try:
        # Check if variable type exists if provided
        variable_type = None
        if payload.variable_type:
            try:
                variable_type = VariableType.objects.get(id=payload.variable_type)

                # Check if user has access to the variable type
                if not variable_type.is_built_in and variable_type.created_by != user:
                    return None, "You don't have permission to use this variable type."
            except VariableType.DoesNotExist:
                return (
                    None,
                    f"Variable type with ID {payload.variable_type} not found.",
                )

        # Create the variable
        variable = Variable(
            # Variable Details
            name=payload.name,
            description=payload.description,
            value=payload.value,
            is_global=payload.is_global,
            # Variable Type
            variable_type=variable_type,
            # Audit
            created_by=user,
            updated_by=user,
        )
        variable.save()
        return variable, None
    except Exception as e:
        return None, f"Error creating variable: {str(e)}"
