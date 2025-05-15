from typing import Optional, Tuple
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.industry.models import Industry
from apps.user.models import User


@transaction.atomic
def update_industry_service(
    industry_id: str,
    user: User,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Tuple[Optional[Industry], Optional[str]]:
    try:
        if not industry_id:
            return None, "Industry ID is required."

        industry = Industry.objects.get(id=industry_id)

        # Update fields if provided
        if name is not None:
            # Check if name would conflict with existing industry
            if name.strip() == "":
                return None, "Industry name cannot be empty."

            existing = (
                Industry.objects.filter(name__iexact=name)
                .exclude(id=industry_id)
                .exists()
            )
            if existing:
                return None, f"Industry with name '{name}' already exists."

            industry.name = name

        if description is not None:
            industry.description = description

        # Update audit information
        industry.updated_by = user

        # Save changes
        industry.save()

        return industry, None

    except ObjectDoesNotExist:
        return None, f"Industry with ID {industry_id} not found."
    except Exception as e:
        return None, f"Error updating industry: {str(e)}"
