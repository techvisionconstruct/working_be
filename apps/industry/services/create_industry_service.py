from typing import Optional, Tuple
from django.db import transaction

from apps.industry.models import Industry
from apps.user.models import User


@transaction.atomic
def create_industry_service(
    name: str, description: str = None, user: User = None
) -> Tuple[Optional[Industry], Optional[str]]:
    try:
        # Validate industry name is not empty
        if not name or name.strip() == "":
            return None, "Industry name is required."

        # Check if an industry with this name already exists
        if Industry.objects.filter(name__iexact=name).exists():
            return None, f"Industry with name '{name}' already exists."

        new_industry = Industry.objects.create(
            name=name,
            description=description,
            created_by=user,
            updated_by=user,
        )

        return new_industry, None

    except Exception as e:
        # Return None for the industry and the error message
        return None, f"Failed to create industry: {str(e)}"
