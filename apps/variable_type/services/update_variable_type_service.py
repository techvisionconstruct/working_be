from typing import Optional, Tuple

from apps.variable_type.models import VariableType
from apps.user.models import User
from apps.variable_type.dto import VariableTypeUpdateRequest


def update_variable_type_service(
    variable_type_id: str, payload: VariableTypeUpdateRequest, user: User
) -> Tuple[Optional[VariableType], Optional[str]]:
    try:
        # Check if the variable type exists
        try:
            variable_type = VariableType.objects.get(id=variable_type_id)
        except VariableType.DoesNotExist:
            return None, f"Variable type with ID {variable_type_id} not found."

        # Check permissions
        if variable_type.is_built_in and not user.is_staff:
            return None, "Cannot modify built-in variable types."

        if variable_type.created_by != user and not user.is_staff:
            return None, "You do not have permission to update this variable type."

        # Update fields that are provided in the payload
        if payload.name is not None:
            variable_type.name = payload.name
        if payload.description is not None:
            variable_type.description = payload.description
        if payload.category is not None:
            variable_type.category = payload.category
        if payload.unit is not None:
            variable_type.unit = payload.unit
        if payload.is_built_in is not None and user.is_staff:
            variable_type.is_built_in = payload.is_built_in

        # Update audit field
        variable_type.updated_by = user

        # Save changes
        variable_type.save()

        return variable_type, None
    except Exception as e:
        return None, f"Error updating variable type: {str(e)}"
