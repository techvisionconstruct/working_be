from ninja import Router, Path
from ninja.errors import HttpError
from apps.industry.services import delete_industry_service
from apps.auth.services.authenticate_service import AuthBearer
from helpers.determine_status_code import determine_status_code

router = Router()


@router.delete("/{industry_id}/", auth=AuthBearer())
def delete_industry_api(
    request, industry_id: str = Path(..., description="Industry ID")
):
    # Delete industry using service
    success, error = delete_industry_service(industry_id=industry_id, user=request.auth)

    # Handle error case
    if not success:
        status_code = determine_status_code(error.get("message", "Industry not found"))
        return {
            "success": False,
            "message": error.get("message", "Industry not found"),
            "errors": [],
        }, status_code

    return {"success": True, "message": "Industry deleted successfully", "errors": []}
