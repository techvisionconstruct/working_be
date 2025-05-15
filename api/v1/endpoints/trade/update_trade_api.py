from ninja import Router, Path

from apps.trade.dto import TradeUpdateRequest, TradeResponse
from apps.trade.services.update_trade_service import update_trade_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Trades"])


@router.put("/{trade_id}/", auth=AuthBearer())
def update_trade_api(
    request,
    payload: TradeUpdateRequest,
    trade_id: str = Path(..., description="Trade ID"),
):
    trade, error = update_trade_service(trade_id, payload, request.auth)

    if error:
        if "not found" in error.lower():
            formatted_error = "Failed to update trade. Trade not found."
        elif "permission" in error.lower():
            formatted_error = "Failed to update trade. You don't have permission."
        else:
            formatted_error = f"Failed to update trade. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully updated trade",
        "data": TradeResponse.from_orm(trade),
    }
