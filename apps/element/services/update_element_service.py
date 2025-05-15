from typing import Optional, Tuple, Dict, Any
from decimal import Decimal

from apps.element.models import Element
from apps.user.models import User
from apps.element.dto import ElementUpdateRequest
from helpers.formula_utils import get_variable_details, evaluate_formula
from helpers.process_base64_image import process_base64_image


def _update_formula_and_calculate_cost(
    formula: str, element_field_name: str, element: Element
) -> None:

    # Set the formula
    setattr(element, f"{element_field_name}_cost_formula", formula)

    # Extract and set variable details
    variable_details = get_variable_details(formula)
    setattr(element, f"{element_field_name}_formula_variables", variable_details)

    # Calculate and set cost if possible
    calculated_cost = evaluate_formula(formula, variable_details)
    if calculated_cost is not None:
        setattr(element, f"{element_field_name}_cost", calculated_cost)


def _update_image(image: str, element: Element) -> Optional[str]:
    """
    Process base64 encoded image and update the element.
    Returns an error message if processing fails, None otherwise.
    """
    if image is not None:
        try:
            if image:
                image_file = process_base64_image(image)
                element.image = image_file
            else:
                # If empty string is provided, clear the image
                element.image = None
            return None
        except Exception as e:
            return f"Error processing image: {str(e)}"
    return None


def _update_variables_and_recalculate_cost(
    variables: Dict[str, Any], element_field_name: str, element: Element
) -> None:
    # Set the variables
    setattr(element, f"{element_field_name}_formula_variables", variables)

    # Get the current formula
    formula = getattr(element, f"{element_field_name}_cost_formula")

    # Recalculate cost if formula exists
    if formula:
        calculated_cost = evaluate_formula(formula, variables)
        if calculated_cost is not None:
            setattr(element, f"{element_field_name}_cost", calculated_cost)


def _update_basic_fields(payload: ElementUpdateRequest, element: Element) -> None:

    if payload.name is not None:
        element.name = payload.name

    if payload.description is not None:
        element.description = payload.description


def _update_markup_and_audit(
    markup: Optional[Decimal], user: User, element: Element
) -> None:

    if markup is not None:
        element.markup = markup

    # Update audit information
    element.updated_by = user


def update_element_service(
    element_id: str, payload: ElementUpdateRequest, user: User
) -> Tuple[Optional[Element], Optional[str]]:

    try:
        # Check if the element exists
        try:
            element = Element.objects.get(id=element_id)
        except Element.DoesNotExist:
            return None, f"Element with ID {element_id} not found."

        # Check permissions
        if element.created_by != user and not user.is_staff:
            return None, "You don't have permission to update this element."

        # Update basic fields (name, description)
        _update_basic_fields(payload, element)

        # Process image if present
        if hasattr(payload, "image"):
            error = _update_image(payload.image, element)
            if error:
                return None, error

        # Process material cost formula updates
        if payload.material_cost_formula is not None:
            _update_formula_and_calculate_cost(
                payload.material_cost_formula, "material", element
            )
        elif payload.material_formula_variables is not None:
            _update_variables_and_recalculate_cost(
                payload.material_formula_variables, "material", element
            )

        # Process labor cost formula updates
        if payload.labor_cost_formula is not None:
            _update_formula_and_calculate_cost(
                payload.labor_cost_formula, "labor", element
            )
        elif payload.labor_formula_variables is not None:
            _update_variables_and_recalculate_cost(
                payload.labor_formula_variables, "labor", element
            )

        # Update markup and audit information
        _update_markup_and_audit(payload.markup, user, element)

        # Save changes
        element.save()

        return element, None
    except Exception as e:
        return None, f"Error updating element: {str(e)}"
