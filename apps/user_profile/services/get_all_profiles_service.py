# filepath: /Users/naigggs/Documents/Projects/service/apps/user_profile/services/get_all_profiles_service.py
from typing import List, Optional, Dict, Tuple
from django.db.models import Q
from django.core.paginator import Paginator

from apps.user_profile.models import Profile
from apps.user.models import User


def get_all_profiles_service(
    user: User, search_query: Optional[str] = None, page: int = 1, page_size: int = 10
) -> Tuple[List[Profile], Dict]:
    """
    Get all profiles with optional filtering and pagination

    Args:
        user: User requesting the profiles
        search_query: Optional search term for name, company, etc.
        page: Page number for pagination
        page_size: Number of profiles per page

    Returns:
        Tuple containing list of profiles and pagination info
    """
    # Base query - staff can see all profiles, normal users see only their own
    if user.is_staff or user.is_superuser:
        query = Q()
    else:
        query = Q(user=user)

    # Add optional search filter
    if search_query:
        query &= (
            Q(user__first_name__icontains=search_query)
            | Q(user__last_name__icontains=search_query)
            | Q(company_name__icontains=search_query)
            | Q(job_title__icontains=search_query)
            | Q(bio__icontains=search_query)
        )

    # Fetch filtered and sorted profiles
    all_profiles = Profile.objects.filter(query).order_by("-created_at")

    # Set up pagination
    paginator = Paginator(all_profiles, page_size)
    total_pages = paginator.num_pages

    # Clamp page number
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages

    current_page_profiles = (
        paginator.get_page(page).object_list if total_pages > 0 else []
    )

    pagination_info = {
        "current_page": page,
        "total_pages": total_pages,
        "page_size": page_size,
        "total_count": paginator.count,
    }

    return current_page_profiles, pagination_info
