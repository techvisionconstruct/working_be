# filepath: /Users/naigggs/Documents/Projects/service/apps/user_profile/services/delete_profile_service.py
from typing import Tuple, Optional, Dict
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.user_profile.models import Profile
from apps.user.models import User


def delete_profile_service(profile_id: str, user: User) -> Tuple[bool, Optional[Dict]]:
    """
    Delete a user profile by its ID

    Args:
        profile_id: ID of the profile to delete
        user: User performing the deletion (for permission check)

    Returns:
        Tuple with success flag (bool) and error message (dict) if applicable
    """
    try:
        if not profile_id:
            return False, {"message": "Profile ID is required."}

        profile = Profile.objects.get(id=profile_id)

        # Check permissions - only the profile owner, staff, or superuser can delete
        if not (user.is_staff or user.is_superuser or profile.user == user):
            return False, {
                "message": "You don't have permission to delete this profile."
            }

        # Store name for confirmation message
        user_name = profile.user.first_name if profile.user else "Unknown user"

        # Delete the profile
        profile.delete()

        # Return success with no error
        return True, None

    except ObjectDoesNotExist:
        # Return failure with error message
        return False, {"message": f"Profile with ID {profile_id} not found."}

    except Exception as e:
        # Return failure with error message for other exceptions
        return False, {"message": f"Failed to delete profile: {str(e)}"}
