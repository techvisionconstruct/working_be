from typing import Optional, Dict, Tuple
from django.db import transaction

from apps.subscription_plan.models import SubscriptionPlan
from apps.user.models import User
from apps.user.choices import UserRole


def admin_create_subscription_plan_service(
    admin_user: User,
    name: str,
    description: Optional[str],
    price: float,
    period: str,
    duration_days: int,
    is_active: bool = True,
) -> Tuple[Optional[Dict], Optional[str]]:
    if admin_user.role != UserRole.ADMIN and not getattr(
        admin_user, "is_superuser", False
    ):
        return (
            None,
            "Permission denied: Only administrators can create subscription plans",
        )
    try:
        with transaction.atomic():
            plan = SubscriptionPlan.objects.create(
                name=name,
                description=description or "",
                price=price,
                period=period,
                duration_days=duration_days,
                is_active=is_active,
                created_by=admin_user,
                updated_by=admin_user,
            )
            plan_data = {
                "id": plan.id,
                "name": plan.name,
                "description": plan.description,
                "price": float(plan.price),
                "period": plan.period,
                "duration_days": plan.duration_days,
                "is_active": plan.is_active,
                "created_at": plan.created_at,
                "updated_at": plan.updated_at,
                "created_by": (
                    {
                        "id": admin_user.id,
                        "email": admin_user.email,
                        "username": admin_user.username,
                        "first_name": admin_user.first_name,
                        "last_name": admin_user.last_name,
                        "role": admin_user.role,
                    }
                    if admin_user
                    else None
                ),
            }
            return plan_data, None
    except Exception as e:
        return None, f"Error creating subscription plan: {str(e)}"
