from ninja import Router
from .get_all_templates_api import router as get_all_templates_api_router
from .get_template_by_id_api import router as get_template_by_id_api_router
from .create_template_api import router as create_template_api_router
from .delete_template_api import router as delete_template_api_router
from .update_template_api import router as update_template_api_router

# Create a combined router
router = Router(tags=["Templates"])

# Add all routes from the list_templates router
router.add_router("/list/", get_all_templates_api_router)
router.add_router("/detail/", get_template_by_id_api_router)
router.add_router("/create/", create_template_api_router)
router.add_router("/update/", update_template_api_router)
router.add_router("/delete/", delete_template_api_router)
