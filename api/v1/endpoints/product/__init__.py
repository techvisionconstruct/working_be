from ninja import Router
from .admin_search_home_depot_products_api import (
    router as admin_search_home_depot_products_router,
)
from .get_all_products_api import router as get_all_products_api_router
from .get_product_by_id_api import router as get_product_by_id_api_router
from .delete_product_api import router as delete_product_api_router
from .delete_duplicate_products_api import (
    router as delete_duplicate_products_api_router,
)


router = Router(tags=["Products"])

router.add_router("/admin/home-depot/search/", admin_search_home_depot_products_router)
router.add_router("/list/", get_all_products_api_router)
router.add_router("/detail/", get_product_by_id_api_router)
router.add_router("/delete/", delete_product_api_router)
router.add_router("/delete-duplicates/", delete_duplicate_products_api_router)
