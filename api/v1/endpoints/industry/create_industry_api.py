from ninja import Router
from ninja.errors import HttpError

from apps.industry.dto import IndustryCreateRequest, IndustryResponse
from apps.industry.services import create_industry_service
from apps.auth.services.authenticate_service import AuthBearer
from helpers.determine_status_code import determine_status_code

router = Router()


@router.post("", auth=AuthBearer())
def create_industry_api(request, payload: IndustryCreateRequest):
    # Create industry using service
    industry, error = create_industry_service(
        name=payload.name, description=payload.description, user=request.auth
    )

    # Handle error case
    if error:
        status_code = determine_status_code(error)
        return {
            "success": False,
            "message": error,
            "errors": [{"field": "name", "message": error}],
            "data": None,
        }, status_code

    return {
        "success": True,
        "message": "Industry created successfully",
        "errors": [],
        "data": IndustryResponse.from_orm(industry),
    }
