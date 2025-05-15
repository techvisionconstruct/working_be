# filepath: /Users/naigggs/Documents/Projects/service/helpers/create_derived_trade.py
from django.db import transaction
from apps.trade.models import Trade
from apps.user.models import User
from apps.template.models import Template
from typing import Optional
from helpers.create_derived_element import create_derived_element
from apps.trade.choices import TradeOrigin


def create_derived_trade(
    source_trade: Trade, user: User, template: Optional[Template] = None
) -> Trade:
    with transaction.atomic():
        # Create a new trade with the same data
        derived_trade = Trade.objects.create(
            name=source_trade.name,
            description=source_trade.description,
            origin=TradeOrigin.DERIVED,
            source=source_trade,
            image=source_trade.image,
            created_by=user,
            updated_by=user,
        )

        # Create derived elements for each element in the source trade
        if source_trade.elements.exists():
            derived_elements = []
            for source_element in source_trade.elements.all():
                derived_element = create_derived_element(
                    source_element, user, derived_trade
                )
                derived_elements.append(derived_element)

            # Set the derived elements on the trade
            derived_trade.elements.set(derived_elements)

        # If a template is provided, associate the trade with it
        if template:
            template.trades.add(derived_trade)

        return derived_trade
