from ninja import Router, Path
from ninja.errors import HttpError

from apps.user_profile.dto import ProfileUpdateRequest, ProfileDetailResponse
from apps.user_profile.services import update_profile_service
from apps.auth.services.authenticate_service import AuthBearer
from helpers.determine_status_code import determine_status_code

router = Router()


@router.put("/{profile_id}/", response=ProfileDetailResponse, auth=AuthBearer())
def update_profile_api(
    request,
    payload: ProfileUpdateRequest,
    profile_id: str = Path(..., description="Profile ID"),
):
    # Update profile using service
    profile, error = update_profile_service(
        profile_id=profile_id, payload=payload, user=request.auth
    )

    # Handle error case
    if error:
        status_code = determine_status_code(error)
        return {"success": False, "message": error, "data": None}, status_code

    return {"success": True, "message": "Profile updated successfully", "data": profile}
