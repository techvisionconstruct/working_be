from typing import Dict, Optional, Tuple

from apps.subscription_plan.models import SubscriptionPlan
from apps.user.models import User
from apps.user.choices import UserRole


def admin_delete_subscription_plan_service(
    admin_user: User,
    subscription_plan_id: str,
) -> Tuple[Optional[Dict], Optional[str]]:
    # Verify admin privileges
    if admin_user.role != UserRole.ADMIN and not getattr(
        admin_user, "is_superuser", False
    ):
        return (
            None,
            "Permission denied: Only administrators can delete subscription plans",
        )

    try:
        # Find the subscription plan to delete
        try:
            plan = SubscriptionPlan.objects.get(id=subscription_plan_id)
        except SubscriptionPlan.DoesNotExist:
            return None, f"Subscription plan with ID {subscription_plan_id} not found"

        # Store plan data before deletion for response
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

        plan.delete()

        return plan_data, None

    except Exception as e:
        return None, f"Error deleting subscription plan: {str(e)}"
