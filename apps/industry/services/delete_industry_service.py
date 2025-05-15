from typing import Tuple, Optional, Dict
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.industry.models import Industry
from apps.user.models import User


@transaction.atomic
def delete_industry_service(
    industry_id: str, user: User
) -> Tuple[bool, Optional[Dict]]:
    try:
        industry = Industry.objects.get(id=industry_id)

        # Check if this industry can be deleted (optional: add additional checks here)
        # For example, if the industry is linked to user profiles, you might want to
        # prevent deletion or implement a soft delete

        # For now, we'll proceed with the deletion
        industry_name = industry.name
        industry.delete()

        # Return success with no error
        return True, None

    except ObjectDoesNotExist:
        # Return failure with error message
        return False, {"message": f"Industry with ID {industry_id} not found"}

    except Exception as e:
        # Return failure with error message for other exceptions
        return False, {"message": f"Failed to delete industry: {str(e)}"}
