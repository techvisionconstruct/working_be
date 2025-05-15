from typing import List, Dict, Optional, Tuple, Any
from django.core.paginator import Paginator
from django.db.models import Q
from apps.subscription_plan.models import SubscriptionPlan
from apps.user.choices import UserRole
from apps.user.models import User


def admin_get_all_subscription_plan_service(
    admin_user: User,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "-created_at",
) -> Tuple[List[Dict], Dict]:
    # Verify admin privileges
    if admin_user.role != UserRole.ADMIN and not getattr(
        admin_user, "is_superuser", False
    ):
        return [], {
            "current_page": 1,
            "total_pages": 0,
            "page_size": page_size,
            "total_count": 0,
        }

    try:
        queryset = SubscriptionPlan.objects.all()

        # Apply search filter (if provided)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        # Apply is_active filter
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        # Apply sorting
        queryset = queryset.order_by(sort_by)

        # Apply pagination
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)

        plans_data = []
        for subscription_plan in page_obj.object_list:
            creator = None
            if (
                hasattr(subscription_plan, "created_by")
                and subscription_plan.created_by
            ):
                creator = {
                    "id": subscription_plan.created_by.id,
                    "email": subscription_plan.created_by.email,
                    "username": subscription_plan.created_by.username,
                    "first_name": subscription_plan.created_by.first_name,
                    "last_name": subscription_plan.created_by.last_name,
                    "role": subscription_plan.created_by.role,
                }
            plans_data.append(
                {
                    "id": subscription_plan.id,
                    "name": subscription_plan.name,
                    "description": subscription_plan.description,
                    "price": float(subscription_plan.price),
                    "period": subscription_plan.period,
                    "duration_days": subscription_plan.duration_days,
                    "is_active": subscription_plan.is_active,
                    "created_at": subscription_plan.created_at,
                    "updated_at": subscription_plan.updated_at,
                    "created_by": creator,
                }
            )

        pagination_info = {
            "current_page": page,
            "total_pages": paginator.num_pages,
            "page_size": page_size,
            "total_count": paginator.count,
        }

        return plans_data, pagination_info

    except Exception as e:
        return [], {
            "current_page": page,
            "total_pages": 0,
            "page_size": page_size,
            "total_count": 0,
        }
