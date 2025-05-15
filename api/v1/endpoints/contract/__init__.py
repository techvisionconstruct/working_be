from ninja import Router
from .get_all_contracts_api import router as get_all_contracts_api_router
from .get_contract_by_id_api import router as get_contract_by_id_api_router
from .delete_contract_api import router as delete_contract_api_router
from .update_contract_api import router as update_contract_api_router
from .create_contract_api import router as create_contract_api_router
from .client_sign_contract_api import router as client_sign_contract_api_router

router = Router(tags=["Contracts"])

router.add_router("/sign/", client_sign_contract_api_router)
router.add_router("/create/", create_contract_api_router)
router.add_router("/delete/", delete_contract_api_router)
router.add_router("/update/", update_contract_api_router)
router.add_router("/list/", get_all_contracts_api_router)
router.add_router("/detail/", get_contract_by_id_api_router)
