# filepath: /Users/naigggs/Documents/Projects/service/apps/user_profile/services/get_profile_by_id_service.py
from typing import Optional, Tuple

from django.core.exceptions import ObjectDoesNotExist

from apps.user_profile.models import Profile
from apps.user.models import User


def get_profile_by_id_service(
    profile_id: str, user: User
) -> Tuple[Optional[Profile], Optional[str]]:
    """
    Get a profile by its ID

    Args:
        profile_id: The ID of the profile to retrieve
        user: The user making the request

    Returns:
        Tuple containing (profile_object, error_message)
        If successful, error_message will be None
        If failed, profile_object will be None and error_message will contain the error
    """
    try:
        if not profile_id:
            return None, "Profile ID is required."

        # Query for the profile
        profile = Profile.objects.get(id=profile_id)

        # Check permissions - only staff/superuser or owner can view a profile
        if not (user.is_staff or user.is_superuser or profile.user == user):
            return None, "You don't have permission to view this profile."

        return profile, None

    except ObjectDoesNotExist:
        return None, f"Profile with ID {profile_id} not found."
    except Exception as e:
        return None, f"Error retrieving profile: {str(e)}"
