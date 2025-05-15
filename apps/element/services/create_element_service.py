from typing import Optional, Tuple
from decimal import Decimal

from apps.element.models import Element
from apps.user.models import User
from apps.element.dto import ElementCreateRequest
from helpers.process_base64_image import process_base64_image
from helpers.formula_utils import get_variable_details, evaluate_formula


def create_element_service(
    payload: ElementCreateRequest, user: User
) -> Tuple[Optional[Element], Optional[str]]:
    try:
        # Handle image if present as base64 string
        image_file = None
        if payload.image:
            try:
                image_file = process_base64_image(payload.image)
            except Exception as e:
                return None, f"Error processing image: {str(e)}"

        # Get variable details with values in array format
        material_details = get_variable_details(payload.material_cost_formula)
        labor_details = get_variable_details(payload.labor_cost_formula)

        # Calculate costs using formulas
        calculated_material_cost = evaluate_formula(
            payload.material_cost_formula, material_details
        )
        calculated_labor_cost = evaluate_formula(
            payload.labor_cost_formula, labor_details
        )

        # Use calculated costs if available, otherwise use the values from payload
        material_cost = calculated_material_cost
        labor_cost = calculated_labor_cost

        # Create the element
        element = Element(
            # Element Details
            name=payload.name,
            description=payload.description,
            image=image_file,
            # Cost Formulas
            material_cost_formula=payload.material_cost_formula,
            material_formula_variables=material_details,
            labor_cost_formula=payload.labor_cost_formula,
            labor_formula_variables=labor_details,
            # Costs
            material_cost=material_cost,
            labor_cost=labor_cost,
            markup=payload.markup,
            # Audit
            created_by=user,
            updated_by=user,
        )
        element.save()
        return element, None
    except Exception as e:
        return None, f"Error creating element: {str(e)}"
