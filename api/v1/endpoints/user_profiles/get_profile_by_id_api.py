from ninja import Router, Path
from ninja.errors import HttpError

from apps.user_profile.dto import ProfileDetailResponse
from apps.user_profile.services import get_profile_by_id_service
from apps.auth.services.authenticate_service import AuthBearer
from helpers.determine_status_code import determine_status_code

router = Router()


@router.get("/{profile_id}/", response=ProfileDetailResponse, auth=AuthBearer())
def get_profile_by_id_api(
    request, profile_id: str = Path(..., description="Profile ID")
):
    # Get profile from service
    profile, error = get_profile_by_id_service(profile_id, request.auth)

    # Handle error case
    if error:
        status_code = determine_status_code(error)
        raise HttpError(status_code, {"success": False, "message": error})

    return {
        "success": True,
        "message": "Profile retrieved successfully",
        "data": profile,
    }
