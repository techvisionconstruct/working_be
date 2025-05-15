# filepath: /Users/naigggs/Documents/Projects/service/apps/user_profile/services/create_profile_service.py
from typing import Optional, Tuple

from django.core.exceptions import ObjectDoesNotExist

from apps.user_profile.models import Profile
from apps.industry.models import Industry
from apps.user.models import User
from apps.user_profile.dto import ProfileCreateRequest


def create_profile_service(
    payload: ProfileCreateRequest, user: User
) -> Tuple[Optional[Profile], Optional[str]]:
    try:
        # Check if profile already exists for this user
        if Profile.objects.filter(user=user).exists():
            return None, f"Profile already exists for this user."

        # Process industry if provided
        industry = None
        if payload.industry_id:
            try:
                industry = Industry.objects.get(id=payload.industry_id)
            except ObjectDoesNotExist:
                return None, f"Industry with ID {payload.industry_id} not found."

        # Create the profile
        profile = Profile.objects.create(
            # User information
            user=user,
            # Basic profile details
            avatar_url=payload.avatar_url,
            bio=payload.bio,
            # Contact Information
            phone_number=payload.phone_number,
            address=payload.address,
            city=payload.city,
            state=payload.state,
            postal_code=payload.postal_code,
            country=payload.country,
            # Professional Information
            company_name=payload.company_name,
            job_title=payload.job_title,
            industry=industry,
            years_of_experience=payload.years_of_experience,
            # Audit
            created_by=user,
            updated_by=user,
        )

        return profile, None

    except Exception as e:
        # Return None for the profile and the error message
        return None, f"Failed to create profile: {str(e)}"
