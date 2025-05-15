# filepath: /Users/naigggs/Documents/Projects/service/api/v1/endpoints/industry/get_industry_by_id_api.py
from ninja import Router, Path
from ninja.errors import HttpError

from apps.industry.dto import IndustryDetailResponse
from apps.industry.services import get_industry_by_id_service
from apps.auth.services.authenticate_service import AuthBearer
from helpers.determine_status_code import determine_status_code

router = Router()


@router.get("/{industry_id}/", response=IndustryDetailResponse, auth=AuthBearer())
def get_industry_by_id_api(
    request, industry_id: str = Path(..., description="Industry ID")
):
    # Get industry from service
    industry, error = get_industry_by_id_service(industry_id)

    # Handle error case
    if error:
        status_code = determine_status_code(error)
        raise HttpError(status_code, {"success": False, "message": error})

    return {
        "success": True,
        "message": "Industry retrieved successfully",
        "data": industry,
    }
