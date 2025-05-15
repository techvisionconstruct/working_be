from ninja import Router, Path
from ninja.errors import HttpError

from apps.user_profile.services import delete_profile_service
from apps.auth.services.authenticate_service import AuthBearer
from helpers.determine_status_code import determine_status_code

router = Router()


@router.delete("/{profile_id}/", auth=AuthBearer())
def delete_profile_api(request, profile_id: str = Path(..., description="Profile ID")):
    # Delete profile using service
    success, error = delete_profile_service(profile_id=profile_id, user=request.auth)

    # Handle error case
    if not success:
        status_code = determine_status_code(error.get("message", "Profile not found"))
        return {
            "success": False,
            "message": error.get("message", "Profile not found"),
        }, status_code

    return {"success": True, "message": "Profile deleted successfully"}
