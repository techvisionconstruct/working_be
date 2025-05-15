from ninja import Router
from ninja.errors import HttpError

from apps.user_profile.dto import ProfileCreateRequest, ProfileResponse
from apps.user_profile.services import create_profile_service
from apps.auth.services.authenticate_service import AuthBearer
from helpers.determine_status_code import determine_status_code

router = Router()


@router.post("/", auth=AuthBearer())
def create_profile_api(request, payload: ProfileCreateRequest):
    # Create profile using service
    profile, error = create_profile_service(payload, request.auth)

    # Handle error case
    if error:
        return ({"success": False, "message": error, "data": None},)

    return {
        "success": True,
        "message": "Profile created successfully",
        "data": ProfileResponse.from_orm(profile),
    }
