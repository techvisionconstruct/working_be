from ninja import Router
from .signin_api import router as signin_api_router
from .signup_api import router as signup_api_router
from .signout_api import router as signout_api_router
from .verify_otp_api import router as verify_otp_api_router

# Create a combined router
router = Router(tags=["Authentication"])

# Add all routes from the signin and signup routers
router.add_router("/signin", signin_api_router)
router.add_router("/signup", signup_api_router)
router.add_router("/signout", signout_api_router)
router.add_router("/verify-otp", verify_otp_api_router)
