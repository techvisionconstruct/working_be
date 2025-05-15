from ninja import NinjaAPI
from .v1.router import router as v1_router

api = NinjaAPI(title="Service API", version="1.0.0")

api.add_router("/v1", v1_router)
