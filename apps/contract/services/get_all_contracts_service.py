from typing import Dict, Tuple, List, Optional
from django.db.models import Q
from django.core.paginator import Paginator

from apps.contract.models import Contract
from apps.user.models import User


def get_all_contracts_service(
    user: User, search_query: Optional[str] = None, page: int = 1, page_size: int = 10
) -> Tuple[List[Contract], Dict]:

    # Base query
    query = Q(created_by=user) | Q(owner=user)

    # Apply search filter if provided
    if search_query:
        search_filter = Q(name__icontains=search_query) | Q(
            description__icontains=search_query
        )
        query &= search_filter

    all_contracts = Contract.objects.filter(query).distinct().order_by("-created_at")

    # Pagination
    paginator = Paginator(all_contracts, page_size)
    total_pages = paginator.num_pages

    # Ensure page is within valid range
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages

    # Get templates for current page
    current_page_contracts = (
        paginator.get_page(page).object_list if total_pages > 0 else []
    )

    # Pagination metadata
    pagination_info = {
        "current_page": page,
        "total_pages": total_pages,
        "page_size": page_size,
        "total_count": paginator.count,
    }

    return current_page_contracts, pagination_info
