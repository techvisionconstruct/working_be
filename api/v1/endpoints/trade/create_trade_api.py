from ninja import Router

from apps.trade.dto import TradeCreateRequest, TradeResponse
from apps.trade.services.create_trade_service import create_trade_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Trades"])


@router.post("/", auth=AuthBearer())
def create_trade_api(request, payload: TradeCreateRequest):
    trade, error = create_trade_service(payload, request.auth)

    if error:
        if "permission" in error.lower():
            formatted_error = "Failed to create trade. You don't have permission."
        else:
            formatted_error = f"Failed to create trade. {error}"
        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully created trade",
        "data": TradeResponse.from_orm(trade),
    }
