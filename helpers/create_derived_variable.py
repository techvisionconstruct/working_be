from django.db import transaction
from apps.variable.models import Variable
from apps.variable.choices import VariableOrigin
from apps.user.models import User
from typing import Tuple, Dict


def create_derived_variable(
    source_variable: Variable, user: User
) -> Tuple[Variable, Dict[str, str]]:

    with transaction.atomic():
        variable = Variable.objects.create(
            name=source_variable.name,
            description=source_variable.description,
            value=source_variable.value,
            is_global=source_variable.is_global,
            origin=VariableOrigin.DERIVED,
            source=source_variable,
            variable_type=source_variable.variable_type,
            created_by=user,
            updated_by=user,
        )

        # Create a mapping of old variable ID to new variable ID
        id_mapping = {str(source_variable.id): str(variable.id)}

        return variable, id_mapping
