from ninja import Router
from .get_all_variable_types_api import router as get_all_variable_type_api_router
from .get_variable_type_by_id_api import router as get_variable_type_by_id_api_router
from .create_variable_type_api import router as create_variable_type_api_router
from .delete_variable_type_api import router as delete_variable_type_api_router
from .update_variable_type_api import router as update_variable_type_api_router

# Create a combined router
router = Router(tags=["Variable Types"])

# Add all routes from the list_variable_types router
router.add_router("/create/", create_variable_type_api_router)
router.add_router("/delete/", delete_variable_type_api_router)
router.add_router("/update/", update_variable_type_api_router)
router.add_router("/list/", get_all_variable_type_api_router)
router.add_router("/detail/", get_variable_type_by_id_api_router)
