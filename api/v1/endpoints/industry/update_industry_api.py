from ninja import Router, Path
from apps.industry.dto import IndustryUpdateRequest, IndustryResponse
from apps.industry.services import update_industry_service
from apps.auth.services.authenticate_service import AuthBearer
from helpers.determine_status_code import determine_status_code

router = Router()


@router.put("/{industry_id}/", auth=AuthBearer())
def update_industry_api(
    request,
    payload: IndustryUpdateRequest,
    industry_id: str = Path(..., description="Industry ID"),
):
    # Update industry using service
    industry, error = update_industry_service(
        industry_id=industry_id,
        user=request.auth,
        name=payload.name,
        description=payload.description,
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
        "message": "Industry updated successfully",
        "errors": [],
        "data": IndustryResponse.from_orm(industry),
    }
