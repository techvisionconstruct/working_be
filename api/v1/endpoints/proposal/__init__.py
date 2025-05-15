from ninja import Router
from .get_all_proposals_api import router as get_all_proposals_api_router
from .get_proposal_by_id_api import router as get_proposal_by_id_api_router
from .get_client_proposal_by_id_api import (
    router as get_client_proposal_by_id_api_router,
)
from .delete_proposal_api import router as delete_proposal_api_router
from .update_proposal_api import router as update_proposal_api_router
from .create_proposal_api import router as create_proposal_api_router
from .send_proposal_to_client_api import router as send_proposal_to_client_api_router
from .update_proposal_template_api import router as update_proposal_template_api_router

router = Router(tags=["Proposals"])

router.add_router("/send/", send_proposal_to_client_api_router)
router.add_router("/create/", create_proposal_api_router)
router.add_router("/delete/", delete_proposal_api_router)
router.add_router("/update/", update_proposal_api_router)
router.add_router("/list/", get_all_proposals_api_router)
router.add_router("/detail/", get_proposal_by_id_api_router)
router.add_router("/detail/", get_client_proposal_by_id_api_router)
router.add_router("/update-template/", update_proposal_template_api_router)
