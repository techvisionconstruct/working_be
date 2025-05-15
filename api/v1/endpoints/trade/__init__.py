from ninja import Router
from .get_all_trades_api import router as get_all_trades_api_router
from .get_trade_by_id_api import router as get_trade_by_id_api_router
from .delete_trade_api import router as delete_trade_api_router
from .create_trade_api import router as create_trade_api_router
from .update_trade_api import router as update_trade_api_router

router = Router(tags=["Trades"])

router.add_router("/list/", get_all_trades_api_router)
router.add_router("/detail/", get_trade_by_id_api_router)
router.add_router("/delete/", delete_trade_api_router)
router.add_router("/create/", create_trade_api_router)
router.add_router("/update/", update_trade_api_router)
