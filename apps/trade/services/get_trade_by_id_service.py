from typing import Optional, Tuple

from apps.trade.models import Trade
from apps.user.models import User


def get_trade_by_id_service(
    trade_id: str, user: User
) -> Tuple[Optional[Trade], Optional[str]]:
    try:
        # Try to find the trade
        trade = Trade.objects.filter(id=trade_id).first()

        # If trade doesn't exist
        if not trade:
            return None, "Trade not found"

        # Check if user has access (user is owner of the trade)
        if trade.created_by != user:
            return None, "You don't have permission to access this trade"

        return trade, None
    except Exception as e:
        return None, f"Error retrieving trade: {str(e)}"
