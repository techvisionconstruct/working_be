from ninja import Router, Path
from django.http import HttpRequest

from apps.subscription_plan.dto import AdminDeleteSubscriptionPlanResponse
from apps.subscription_plan.services.admin.admin_delete_subscription_plan_service import (
    admin_delete_subscription_plan_service,
)
from apps.user.choices import UserRole
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Subscription Plan"])


@router.delete(
    "/{subscription_plan_id}/",
    response=AdminDeleteSubscriptionPlanResponse,
    auth=AuthBearer(),
)
def admin_delete_subscription_plan_api(
    request: HttpRequest,
    subscription_plan_id: str = Path(..., description="Subscription Plan ID"),
):
    # Check if user is authenticated and has admin privileges
    if not request.auth or request.auth.role != UserRole.ADMIN:
        return {
            "success": False,
            "message": "Failed to delete subscription plan. Insufficient permissions.",
            "errors": [
                {
                    "field": "general",
                    "message": "Only administrators can delete subscription plans",
                }
            ],
            "data": None,
        }

    # Call service to delete subscription plan
    plan_data, error = admin_delete_subscription_plan_service(
        admin_user=request.auth,
        subscription_plan_id=subscription_plan_id,
    )

    # Handle error response
    if error:
        status_message = (
            "Subscription plan not found" if "not found" in error else error
        )

        return {
            "success": False,
            "message": f"Failed to delete subscription plan. {status_message}",
            "errors": [{"field": "general", "message": error}],
            "data": None,
        }

    # Success response
    return {
        "success": True,
        "message": "Successfully deleted subscription plan",
        "errors": [],
        "data": None,
    }
