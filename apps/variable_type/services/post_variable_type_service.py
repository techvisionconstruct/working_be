# filepath: /Users/naigggs/Documents/Projects/service/apps/variable_type/services/post_variable_type_service.py
from typing import Optional, Tuple

from apps.variable_type.models import VariableType
from apps.user.models import User
from apps.variable_type.dto import VariableTypeCreateRequest


def post_variable_type_service(
    payload: VariableTypeCreateRequest, user: User
) -> Tuple[Optional[VariableType], Optional[str]]:
    print("Payload:", payload)
    try:
        variable_type = VariableType(
            # Variable Type Details
            name=payload.name,
            description=payload.description,
            category=payload.category,
            unit=payload.unit,
            is_built_in=payload.is_built_in,
            # Audit
            created_by=user,
            updated_by=user,
        )
        variable_type.save()
        return variable_type, None
    except Exception as e:
        return None, f"Error creating variable type: {str(e)}"
