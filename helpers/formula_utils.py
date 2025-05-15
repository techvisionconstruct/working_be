from typing import List, Dict, Any, Optional, Tuple, Dict
import re
import math
from decimal import Decimal
from apps.variable.models import Variable


def extract_variable_ids(formula: str) -> List[str]:
    if not formula:
        return []

    pattern = r"\{(\w+)[\s\}]"
    matches = re.findall(pattern, formula)
    return matches


def get_variable_details(formula: str) -> List[Dict[str, Any]]:
    if not formula:
        return []

    variable_ids = extract_variable_ids(formula)
    if not variable_ids:
        return []

    # Fetch variable details from database
    variables = Variable.objects.filter(id__in=variable_ids)

    # Create list of variable details
    variable_details = []
    for variable in variables:
        variable_details.append(
            {
                "id": variable.id,
                "name": variable.name,
                "value": float(variable.value) if variable.value is not None else 0.0,
            }
        )

    return variable_details


def update_formula_with_variable_mappings(
    formula: str, variable_id_mapping: Dict[str, str]
) -> Tuple[str, bool]:

    if not formula or not variable_id_mapping:
        return formula, False

    # Make a copy of the original formula for comparison
    updated_formula = formula

    # Replace all variable IDs in the formula
    for old_id, new_id in variable_id_mapping.items():
        # Make sure to match variable IDs within curly braces {id}
        updated_formula = updated_formula.replace(f"{{{old_id}}}", f"{{{new_id}}}")

    # Return the updated formula and whether it changed
    return updated_formula, updated_formula != formula


def update_element_formulas(element, variable_id_mapping: Dict[str, str]) -> bool:
    formula_updated = False

    # Update material cost formula
    if element.material_cost_formula:
        try:
            updated_formula, was_updated = update_formula_with_variable_mappings(
                element.material_cost_formula, variable_id_mapping
            )

            if was_updated:
                element.material_cost_formula = updated_formula
                formula_updated = True

                # Update material formula variables
                material_variable_details = get_variable_details(updated_formula)
                if material_variable_details:
                    element.material_formula_variables = material_variable_details
        except Exception as e:
            # Continue with other updates if one fails
            pass

    # Update labor cost formula
    if element.labor_cost_formula:
        try:
            updated_formula, was_updated = update_formula_with_variable_mappings(
                element.labor_cost_formula, variable_id_mapping
            )

            if was_updated:
                element.labor_cost_formula = updated_formula
                formula_updated = True

                # Update labor formula variables
                labor_variable_details = get_variable_details(updated_formula)
                if labor_variable_details:
                    element.labor_formula_variables = labor_variable_details
        except Exception as e:
            # Continue with other updates if one fails
            pass

    return formula_updated


def evaluate_formula(
    formula: str, variable_details: List[Dict[str, Any]]
) -> Optional[Decimal]:

    if not formula or not variable_details:
        return None

    # Create a copy of the formula for substitution
    evaluated_formula = formula

    # Replace each variable with its value
    for var_info in variable_details:
        var_id = var_info["id"]
        value = var_info["value"]
        # Replace {variable_id} with its value
        evaluated_formula = evaluated_formula.replace(f"{{{var_id}}}", str(value))

    try:
        # Safely evaluate the mathematical expression
        # First remove any remaining curly braces that weren't replaced
        evaluated_formula = re.sub(r"\{[^}]*\}", "0", evaluated_formula)

        # Use safer eval with math functions available
        # Create a safe environment with only math operations
        safe_dict = {
            "abs": abs,
            "max": max,
            "min": min,
            "pow": pow,
            "round": round,
            "math": math,
        }

        result = eval(evaluated_formula, {"__builtins__": {}}, safe_dict)
        return Decimal(str(result))
    except Exception as e:
        print(f"Error evaluating formula: {evaluated_formula}, Error: {e}")
        return None
