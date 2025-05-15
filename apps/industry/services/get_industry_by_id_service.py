from typing import Optional, Tuple

from django.core.exceptions import ObjectDoesNotExist

from apps.industry.models import Industry


def get_industry_by_id_service(
    industry_id: str,
) -> Tuple[Optional[Industry], Optional[str]]:
    try:
        if not industry_id:
            return None, "Industry ID is required."

        industry = Industry.objects.get(id=industry_id)
        return industry, None

    except ObjectDoesNotExist:
        return None, f"Industry with ID {industry_id} not found."
    except Exception as e:
        return None, f"Error retrieving industry: {str(e)}"
