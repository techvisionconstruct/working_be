# filepath: /Users/naigggs/Documents/Projects/service/apps/user_profile/services/update_profile_service.py
from typing import Optional, Tuple
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.user_profile.models import Profile
from apps.industry.models import Industry
from apps.user.models import User
from apps.user_profile.dto import ProfileUpdateRequest


def update_profile_service(
    profile_id: str, payload: ProfileUpdateRequest, user: User
) -> Tuple[Optional[Profile], Optional[str]]:
    try:
        if not profile_id:
            return None, "Profile ID is required."

        # Get the profile
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            return None, f"Profile with ID {profile_id} not found."

        # Check permissions - only the profile owner, staff, or superuser can update
        if not (user.is_staff or user.is_superuser or profile.user == user):
            return None, "You don't have permission to update this profile."

        # Update industry if provided
        if hasattr(payload, "industry_id") and payload.industry_id is not None:
            if payload.industry_id:
                try:
                    industry = Industry.objects.get(id=payload.industry_id)
                    profile.industry = industry
                except ObjectDoesNotExist:
                    return None, f"Industry with ID {payload.industry_id} not found."
            else:
                profile.industry = None

        # Update basic profile fields if provided
        if hasattr(payload, "avatar_url"):
            profile.avatar_url = payload.avatar_url

        if hasattr(payload, "bio"):
            profile.bio = payload.bio

        # Update contact information
        if hasattr(payload, "phone_number"):
            profile.phone_number = payload.phone_number

        if hasattr(payload, "address"):
            profile.address = payload.address

        if hasattr(payload, "city"):
            profile.city = payload.city

        if hasattr(payload, "state"):
            profile.state = payload.state

        if hasattr(payload, "postal_code"):
            profile.postal_code = payload.postal_code

        if hasattr(payload, "country"):
            profile.country = payload.country

        # Update professional information
        if hasattr(payload, "company_name"):
            profile.company_name = payload.company_name

        if hasattr(payload, "job_title"):
            profile.job_title = payload.job_title

        if hasattr(payload, "years_of_experience"):
            profile.years_of_experience = payload.years_of_experience

        # Update audit information
        profile.updated_by = user

        # Save changes
        profile.save()

        return profile, None

    except Exception as e:
        return None, f"Error updating profile: {str(e)}"
