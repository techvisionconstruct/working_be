from ninja import Router
from .admin_get_all_subscription_plan_api import (
    router as admin_get_all_subscription_plan_router,
)
from .admin_get_subscription_plan_by_id_api import (
    router as admin_get_subscription_plan_by_id_router,
)
from .admin_create_subscription_plan_api import (
    router as admin_create_subscription_plan_router,
)
from .admin_update_subscription_plan_api import (
    router as admin_update_subscription_plan_router,
)
from .admin_delete_subscription_plan_api import (
    router as admin_delete_subscription_plan_router,
)

# Create a combined router
router = Router(tags=["Subscription Plan"])

# Routes
router.add_router("/admin/list", admin_get_all_subscription_plan_router)
router.add_router("/admin/detail", admin_get_subscription_plan_by_id_router)
router.add_router("/admin/create", admin_create_subscription_plan_router)
router.add_router("/admin/update", admin_update_subscription_plan_router)
router.add_router("/admin/delete", admin_delete_subscription_plan_router)
