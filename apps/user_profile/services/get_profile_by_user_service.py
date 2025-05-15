# filepath: /Users/naigggs/Documents/Projects/service/apps/user_profile/services/get_profile_by_user_service.py
from typing import Optional, Tuple

from django.core.exceptions import ObjectDoesNotExist

from apps.user_profile.models import Profile
from apps.user.models import User


def get_profile_by_user_service(user: User) -> Tuple[Optional[Profile], Optional[str]]:

    try:
        if not user:
            return None, "User is required."

        profile = Profile.objects.filter(user=user).first()

        if not profile:
            return None, f"Profile for user {user.id} not found."

        return profile, None

    except Exception as e:
        return None, f"Error retrieving user profile: {str(e)}"
