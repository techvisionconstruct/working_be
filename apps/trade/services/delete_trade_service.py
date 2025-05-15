from typing import Optional, Tuple

from apps.trade.models import Trade
from apps.user.models import User


def delete_trade_service(trade_id: str, user: User) -> Tuple[bool, Optional[str]]:
    try:
        # Check if the trade exists
        try:
            trade = Trade.objects.get(id=trade_id)
        except Trade.DoesNotExist:
            return False, f"Trade with ID {trade_id} not found."

        # Check permissions
        if trade.created_by != user:
            return False, "You don't have permission to delete this trade."

        # Check if the trade is associated with any templates
        if trade.templates.exists():
            return (
                False,
                "Cannot delete this trade as it is used in one or more templates.",
            )

        # Record the user who performed the deletion (for audit logs if needed)
        trade.updated_by = user

        # Delete the trade
        trade.delete()

        return True, None
    except Exception as e:
        return False, f"Error deleting trade: {str(e)}"
