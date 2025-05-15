# filepath: /Users/naigggs/Documents/Projects/service/api/v1/endpoints/industry/__init__.py
from ninja import Router

from .get_all_industries_api import router as get_all_industries_router
from .get_industry_by_id_api import router as get_industry_by_id_router
from .create_industry_api import router as create_industry_router
from .update_industry_api import router as update_industry_router
from .delete_industry_api import router as delete_industry_router

router = Router(tags=["Industries"])
router.add_router("/list/", get_all_industries_router)
router.add_router("/detail/", get_industry_by_id_router)
router.add_router("/create/", create_industry_router)
router.add_router("/update/", update_industry_router)
router.add_router("/delete/", delete_industry_router)
