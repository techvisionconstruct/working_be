# filepath: /Users/naigggs/Documents/Projects/service/helpers/create_derived_element.py
from django.db import transaction
from apps.element.models import Element
from apps.user.models import User
from apps.trade.models import Trade
from typing import Optional
from apps.element.choices import ElementOrigin


def create_derived_element(
    source_element: Element, user: User, trade: Optional[Trade] = None
) -> Element:

    with transaction.atomic():
        # Create a new element with the same data
        derived_element = Element.objects.create(
            name=source_element.name,
            description=source_element.description,
            image=source_element.image,
            origin=ElementOrigin.DERIVED,
            source=source_element,
            # Cost formulas
            material_cost_formula=source_element.material_cost_formula,
            material_formula_variables=source_element.material_formula_variables,
            labor_cost_formula=source_element.labor_cost_formula,
            labor_formula_variables=source_element.labor_formula_variables,
            material_cost=source_element.material_cost,
            labor_cost=source_element.labor_cost,
            markup=source_element.markup,
            # Audit
            created_by=user,
            updated_by=user,
        )

        return derived_element
