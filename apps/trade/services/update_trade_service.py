from typing import Optional, Tuple

from apps.trade.models import Trade
from apps.user.models import User
from apps.trade.dto import TradeUpdateRequest
from apps.element.models import Element
from helpers.process_base64_image import process_base64_image


def update_trade_service(
    trade_id: str, payload: TradeUpdateRequest, user: User
) -> Tuple[Optional[Trade], Optional[str]]:
    try:
        # Check if the trade exists
        try:
            trade = Trade.objects.get(id=trade_id)
        except Trade.DoesNotExist:
            return None, f"Trade with ID {trade_id} not found."

        # Check permissions
        if trade.created_by != user:
            return None, "You don't have permission to update this trade."

        # Handle image if present as base64 string
        if "image" in payload:
            image = payload.pop("image")
            if image:
                try:
                    image_file = process_base64_image(image)
                    trade.image = image_file
                except Exception as e:
                    return None, f"Error processing image: {str(e)}"

        # Update basic fields if provided
        if payload.name is not None:
            trade.name = payload.name

        if payload.description is not None:
            trade.description = payload.description

        # Update elements if provided
        if payload.elements is not None:
            if payload.elements:
                # The elements are already provided as IDs (strings)
                elements = Element.objects.filter(
                    id__in=payload.elements, created_by=user
                )
                trade.elements.set(elements)
            else:
                # If elements list is empty, clear the relationship
                trade.elements.clear()

        # Update audit information
        trade.updated_by = user

        # Save changes
        trade.save()

        return trade, None
    except Exception as e:
        return None, f"Error updating trade: {str(e)}"
