from typing import Optional, Tuple

from apps.trade.models import Trade
from apps.user.models import User
from apps.trade.dto import TradeCreateRequest
from apps.element.models import Element
from helpers.process_base64_image import process_base64_image


def create_trade_service(
    payload: TradeCreateRequest, user: User
) -> Tuple[Optional[Trade], Optional[str]]:
    try:
        # Process image if provided
        image_file = None
        if payload.image:
            try:
                image_file = process_base64_image(payload.image)
            except Exception as e:
                return None, f"Error processing image: {str(e)}"

        trade = Trade(
            # Trade Details
            name=payload.name,
            description=payload.description,
            image=image_file,
            # Audit
            created_by=user,
            updated_by=user,
        )
        trade.save()

        # Add elements if provided
        if payload.elements:
            # The elements are already provided as IDs (strings)
            elements = Element.objects.filter(id__in=payload.elements, created_by=user)
            trade.elements.set(elements)

        return trade, None
    except Exception as e:
        return None, f"Error creating trade: {str(e)}"
