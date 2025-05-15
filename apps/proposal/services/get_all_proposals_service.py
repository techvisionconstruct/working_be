from typing import List, Optional, Dict, Tuple
from django.db.models import Q
from django.core.paginator import Paginator

from apps.proposal.models import Proposal
from apps.user.models import User


def get_all_proposals_service(
    user: User, search_query: Optional[str] = None, page: int = 1, page_size: int = 10
) -> Tuple[List[Proposal], Dict]:
    # Base query: user's own proposal
    query = Q(created_by=user)

    # Add search filter if provided
    if search_query:
        search_filter = Q(name__icontains=search_query) | Q(
            description__icontains=search_query
        )
        query &= search_filter

    # Fetch templates matching criteria
    all_proposals = Proposal.objects.filter(query).distinct().order_by("-created_at")

    # Create paginator
    paginator = Paginator(all_proposals, page_size)
    total_pages = paginator.num_pages

    # Ensure page is within valid range
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages

    # Get templates for current page
    current_page_proposals = (
        paginator.get_page(page).object_list if total_pages > 0 else []
    )

    # Pagination metadata
    pagination_info = {
        "current_page": page,
        "total_pages": total_pages,
        "page_size": page_size,
        "total_count": paginator.count,
    }

    return current_page_proposals, pagination_info
