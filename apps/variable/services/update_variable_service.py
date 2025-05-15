from typing import Optional, Tuple
from helpers.formula_utils import get_variable_details, evaluate_formula
from apps.variable.models import Variable
from apps.user.models import User
from apps.variable.dto import VariableUpdateRequest
from apps.variable_type.models import VariableType

def _update_formula_and_calculate_cost(
    formula: str, variable_field_name: str, variable: Variable
) -> None:
    # Check for self-reference in the formula
    if variable.id in formula:
        raise ValueError("A variable formula cannot reference itself.")

    setattr(variable, "formula", formula)
    variable_details = get_variable_details(formula)
    setattr(variable, f"{variable_field_name}_formula_variables", variable_details)
    calculated_cost = evaluate_formula(formula, variable_details)
    if calculated_cost is not None:
        setattr(variable, f"{variable_field_name}", calculated_cost)

def _update_dependent_variables(updated_variable: Variable, visited=None):
    if visited is None:
        visited = set()
    if updated_variable.id in visited:
        raise ValueError("Circular dependency detected in variable formulas.")
    visited.add(updated_variable.id)

    dependents = Variable.objects.filter(formula__icontains=updated_variable.id)
    for dependent in dependents:
        if dependent.id == updated_variable.id:
            raise ValueError("A variable formula cannot reference itself.")
        if updated_variable.id in dependent.formula:
            _update_formula_and_calculate_cost(
                dependent.formula, "value", dependent
            )
            dependent.save()
            _update_dependent_variables(dependent, visited)

def update_variable_service(
    variable_id: str, payload: VariableUpdateRequest, user: User
) -> Tuple[Optional[Variable], Optional[str]]:
    try:
        try:
            variable = Variable.objects.get(id=variable_id)
        except Variable.DoesNotExist:
            return None, f"Variable with ID {variable_id} not found."

        if variable.created_by != user and not user.is_staff:
            return None, "You do not have permission to update this variable."

        if payload.variable_type is not None:
            if payload.variable_type:
                try:
                    variable_type = VariableType.objects.get(id=payload.variable_type)
                    if (
                        not variable_type.is_built_in
                        and variable_type.created_by != user
                    ):
                        return (
                            None,
                            "You don't have permission to use this variable type.",
                        )
                    variable.variable_type = variable_type
                except VariableType.DoesNotExist:
                    return (
                        None,
                        f"Variable type with ID {payload.variable_type_id} not found.",
                    )
            else:
                variable.variable_type = None

        if payload.name is not None:
            variable.name = payload.name

        if payload.description is not None:
            variable.description = payload.description

        value_updated = False
        if payload.value is not None:
            variable.value = payload.value
            value_updated = True

        if payload.is_global is not None and user.is_staff:
            variable.is_global = payload.is_global

        if payload.formula is not None:
            variable.formula = payload.formula
            _update_formula_and_calculate_cost(
                payload.formula, "value", variable
            )

        variable.updated_by = user
        variable.save()

        # If value was updated, update all dependent variables
        if value_updated:
            _update_dependent_variables(variable)

        return variable, None
    except Exception as e:
        return None, f"Error updating variable: {str(e)}"
