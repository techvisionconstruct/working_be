from typing import Optional, Dict, Tuple
from django.db import transaction

from apps.subscription_plan.models import SubscriptionPlan
from apps.user.models import User
from apps.user.choices import UserRole


def admin_update_subscription_plan_service(
    admin_user: User,
    subscription_plan_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    period: Optional[str] = None,
    duration_days: Optional[int] = None,
    is_active: Optional[bool] = None,
) -> Tuple[Optional[Dict], Optional[str]]:
    if admin_user.role != UserRole.ADMIN and not getattr(
        admin_user, "is_superuser", False
    ):
        return (
            None,
            "Permission denied: Only administrators can update subscription plans",
        )

    try:
        try:
            plan = SubscriptionPlan.objects.get(id=subscription_plan_id)
        except SubscriptionPlan.DoesNotExist:
            return None, f"Subscription plan with ID {subscription_plan_id} not found"

        with transaction.atomic():
            if name is not None:
                plan.name = name
            if description is not None:
                plan.description = description
            if price is not None:
                plan.price = price
            if period is not None:
                plan.period = period
            if duration_days is not None:
                plan.duration_days = duration_days
            if is_active is not None:
                plan.is_active = is_active

            plan.updated_by = admin_user
            plan.save()

            creator = None
            if hasattr(plan, "created_by") and plan.created_by:
                creator = {
                    "id": plan.created_by.id,
                    "email": plan.created_by.email,
                    "username": plan.created_by.username,
                    "first_name": plan.created_by.first_name,
                    "last_name": plan.created_by.last_name,
                    "role": plan.created_by.role,
                }

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
                "created_by": creator,
            }
            return plan_data, None

    except Exception as e:
        return None, f"Error updating subscription plan: {str(e)}"
