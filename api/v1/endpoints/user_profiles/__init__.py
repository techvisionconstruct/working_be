# filepath: /Users/naigggs/Documents/Projects/service/api/v1/endpoints/user_profiles/__init__.py
from ninja import Router

from .get_all_profiles_api import router as get_all_profiles_router
from .get_profile_by_id_api import router as get_profile_by_id_router
from .get_current_user_profile_api import router as get_current_user_profile_router
from .create_profile_api import router as create_profile_router
from .update_profile_api import router as update_profile_router
from .delete_profile_api import router as delete_profile_router

router = Router(tags=["User Profiles"])
router.add_router("/list/", get_all_profiles_router)
router.add_router("/detail/", get_profile_by_id_router)
router.add_router("/me/", get_current_user_profile_router)
router.add_router("/create/", create_profile_router)
router.add_router("/update/", update_profile_router)
router.add_router("/delete/", delete_profile_router)
