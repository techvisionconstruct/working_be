from ninja import Router
from ninja.errors import HttpError

from apps.user_profile.dto import ProfileDetailResponse
from apps.user_profile.services import get_profile_by_user_service
from apps.auth.services.authenticate_service import AuthBearer
from helpers.determine_status_code import determine_status_code

router = Router()


@router.get("", response=ProfileDetailResponse, auth=AuthBearer())
def get_current_user_profile_api(request):
    # Get profile from service
    profile, error = get_profile_by_user_service(request.auth)

    # Handle error case
    if error:
        status_code = determine_status_code(error)
        raise HttpError(status_code, {"success": False, "message": error})

    return {
        "success": True,
        "message": "Profile retrieved successfully",
        "data": profile,
    }
