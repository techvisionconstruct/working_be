from ninja import Router, Path

from apps.trade.dto import TradeDetailResponse
from apps.trade.services.get_trade_by_id_service import get_trade_by_id_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Trades"])


@router.get("/{trade_id}/", response=TradeDetailResponse, auth=AuthBearer())
def get_trade_by_id_api(request, trade_id: str = Path(..., description="Trade ID")):
    trade, error = get_trade_by_id_service(trade_id, request.auth)

    if error:
        if "not found" in error.lower():
            formatted_error = f"Failed to retrieve trade. Trade not found."
        elif "permission" in error.lower():
            formatted_error = f"Failed to access trade. You don't have permission."
        else:
            formatted_error = f"Failed to retrieve trade. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully retrieved trade",
        "data": trade,
    }
