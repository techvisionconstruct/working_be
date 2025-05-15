from typing import Dict, Optional, Tuple
from apps.subscription_plan.models import SubscriptionPlan
from apps.user.models import User
from apps.user.choices import UserRole


def admin_get_subscription_plan_by_id_service(
    admin_user: User,
    subscription_plan_id: str,
) -> Tuple[Optional[Dict], Optional[str]]:
    # Verify admin privileges
    if admin_user.role != UserRole.ADMIN and not getattr(
        admin_user, "is_superuser", False
    ):
        return (
            None,
            "Permission denied: Only administrators can view subscription plan details",
        )

    try:
        # Get the subscription plan
        try:
            subscription_plan = SubscriptionPlan.objects.get(id=subscription_plan_id)
        except SubscriptionPlan.DoesNotExist:
            return None, f"Subscription plan with ID {subscription_plan_id} not found"

        # Get creator info if available
        creator = None
        if hasattr(subscription_plan, "created_by") and subscription_plan.created_by:
            creator = {
                "id": subscription_plan.created_by.id,
                "email": subscription_plan.created_by.email,
                "username": subscription_plan.created_by.username,
                "first_name": subscription_plan.created_by.first_name,
                "last_name": subscription_plan.created_by.last_name,
                "role": subscription_plan.created_by.role,
            }

        subscription_plan_data = {
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

        return subscription_plan_data, None

    except Exception as e:
        return None, f"Error retrieving subscription plan: {str(e)}"
