from ninja import Router
from .admin_create_user_api import router as admin_create_user_api_router
from .admin_get_all_user_api import router as admin_get_all_user_api_router
from .admin_get_user_by_id_api import router as admin_get_user_by_id_api_router
from .admin_update_user_api import router as admin_update_user_api_router
from .admin_delete_user_api import router as admin_delete_user_api_router


router = Router(tags=["Users"])

# Separate routes for different operations to avoid method conflicts
router.add_router("/admin/create", admin_create_user_api_router)
router.add_router("/admin/list", admin_get_all_user_api_router)
router.add_router("/admin/detail", admin_get_user_by_id_api_router)
router.add_router("/admin/update", admin_update_user_api_router)
router.add_router("/admin/delete", admin_delete_user_api_router)
