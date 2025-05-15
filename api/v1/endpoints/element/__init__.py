from ninja import Router
from .get_all_elements_api import router as get_all_elements_api_router
from .get_element_by_id_api import router as get_element_by_id_api_router
from .delete_element_api import router as delete_element_api_router
from .create_element_api import router as create_element_api_router
from .update_element_api import router as update_element_api_router

router = Router(tags=["Elements"])

router.add_router("/list/", get_all_elements_api_router)
router.add_router("/detail/", get_element_by_id_api_router)
router.add_router("/delete/", delete_element_api_router)
router.add_router("/create/", create_element_api_router)
router.add_router("/update/", update_element_api_router)
