from ninja import Router, Path

from apps.trade.services.delete_trade_service import delete_trade_service
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Trades"])


@router.delete("/{trade_id}/", auth=AuthBearer())
def delete_trade_api(request, trade_id: str = Path(..., description="Trade ID")):
    success, error = delete_trade_service(trade_id, request.auth)

    if not success:
        if "not found" in error.lower():
            formatted_error = "Failed to delete trade. Trade not found."
        elif "permission" in error.lower():
            formatted_error = "Failed to delete trade. You don't have permission."
        elif "used in" in error.lower():
            formatted_error = (
                "Failed to delete trade. It is used in one or more templates."
            )
        else:
            formatted_error = f"Failed to delete trade. {error}"

        return {"success": False, "message": formatted_error, "data": None}

    return {
        "success": True,
        "message": "Successfully deleted trade",
        "data": None,
    }
