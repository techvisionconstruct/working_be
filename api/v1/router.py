from ninja import Router
from .endpoints.auth import router as auth_router
from .endpoints.template import router as template_router
from .endpoints.variable_type import router as variable_type_router
from .endpoints.variable import router as variable_router
from .endpoints.user import router as user_router
from .endpoints.element import router as element_router
from .endpoints.trade import router as trade_router
from .endpoints.variable_type import router as variable_type_router
from .endpoints.proposal import router as proposal_router
from .endpoints.subscription_plan import router as subscription_plan_router
from .endpoints.contract import router as contract_router
from .endpoints.product import router as product_router
from .endpoints.jwt import router as jwt_router
from .endpoints.industry import router as industry_router
from .endpoints.user_profiles import router as user_profiles_router


router = Router()

# Register auth endpoints
router.add_router("/auth", auth_router)
router.add_router("/templates", template_router)
router.add_router("/variable-types", variable_type_router)
router.add_router("/variables", variable_router)
router.add_router("/users", user_router)
router.add_router("/subscription-plans", subscription_plan_router)
router.add_router("/elements", element_router)
router.add_router("/trades", trade_router)
router.add_router("/proposals", proposal_router)
router.add_router("/contracts", contract_router)
router.add_router("/products", product_router)
router.add_router("/jwt", jwt_router)
router.add_router("/industries", industry_router)
router.add_router("/user-profiles", user_profiles_router)
