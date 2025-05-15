from typing import List, Dict, Optional, Tuple
from django.db.models import Q
from django.core.paginator import Paginator
import logging

from apps.user.models import User
from apps.user.choices import UserRole

logger = logging.getLogger(__name__)


def admin_get_all_users_service(
    admin_user: User,
    search: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_staff: Optional[bool] = None,
    is_superuser: Optional[bool] = None,
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "-created_at",
) -> Tuple[List[Dict], Dict]:
    # Verify admin privileges
    if admin_user.role != UserRole.ADMIN and not admin_user.is_superuser:
        return [], {
            "current_page": 1,
            "total_pages": 0,
            "page_size": page_size,
            "total_count": 0,
        }

    try:
        # Start with all users
        queryset = User.objects.all()

        # Apply search filter (if provided)
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(username__icontains=search)
            )

        # Apply filters - MAKE SURE FILTERS AREN'T TOO RESTRICTIVE
        if role:
            queryset = queryset.filter(role=role)
            logger.info(f"Filtering by role: {role}, count: {queryset.count()}")

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
            logger.info(
                f"Filtering by is_active: {is_active}, count: {queryset.count()}"
            )

        if is_staff is not None:
            queryset = queryset.filter(is_staff=is_staff)
            logger.info(f"Filtering by is_staff: {is_staff}, count: {queryset.count()}")

        if is_superuser is not None:
            queryset = queryset.filter(is_superuser=is_superuser)
            logger.info(
                f"Filtering by is_superuser: {is_superuser}, count: {queryset.count()}"
            )

        # Apply sorting
        queryset = queryset.order_by(sort_by)

        # Apply pagination
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)

        # Prepare user data
        users_data = []
        for user in page_obj.object_list:
            # Get creator info if available - FIXED THIS PART
            creator = None
            # Check if the attribute exists using hasattr to avoid attribute errors
            if hasattr(user, "created_by") and user.created_by:
                creator = {
                    "id": user.created_by.id,
                    "email": user.created_by.email,
                    "username": user.created_by.username,
                    "first_name": user.created_by.first_name,
                    "last_name": user.created_by.last_name,
                    "role": user.created_by.role,
                }

            users_data.append(
                {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "is_active": user.is_active,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                    "created_by": creator,
                }
            )

        # Simplified pagination metadata
        pagination_info = {
            "current_page": page,
            "total_pages": paginator.num_pages,
            "page_size": page_size,
            "total_count": paginator.count,
        }

        return users_data, pagination_info

    except Exception as e:
        return [], {
            "current_page": page,
            "total_pages": 0,
            "page_size": page_size,
            "total_count": 0,
        }
