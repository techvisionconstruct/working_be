from typing import List, Optional, Dict, Tuple
from django.db.models import Q
from django.core.paginator import Paginator

from apps.product.models import Product
from apps.user.models import User


def get_all_products_service(
    user: User, search_query: Optional[str] = None, page: int = 1, page_size: int = 10
) -> Tuple[List[Product], Dict]:
    # Base query: only products created by the current user
    query = Q(created_by=user)

    # Add optional search filter
    if search_query:
        query &= Q(search_term__icontains=search_query) | Q(
            title__icontains=search_query
        )

    # Fetch filtered and sorted products
    all_products = Product.objects.filter(query).order_by("-created_at")

    # Set up pagination
    paginator = Paginator(all_products, page_size)
    total_pages = paginator.num_pages

    # Clamp page number
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages

    current_page_products = (
        paginator.get_page(page).object_list if total_pages > 0 else []
    )

    pagination_info = {
        "current_page": page,
        "total_pages": total_pages,
        "page_size": page_size,
        "total_count": paginator.count,
    }

    return current_page_products, pagination_info
