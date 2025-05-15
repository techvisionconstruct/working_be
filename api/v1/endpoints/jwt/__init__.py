from ninja import Router
from .refresh_token_api import router as refresh_token_router

router = Router(tags=["JWT"])

router.add_router("/refresh-token/", refresh_token_router)
