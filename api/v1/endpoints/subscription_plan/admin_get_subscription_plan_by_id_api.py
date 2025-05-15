from ninja import Router, Path
from django.http import HttpRequest

from helpers.dto import ErrorItem
from apps.subscription_plan.dto import AdminSubscriptionPlanDetailResponse
from apps.subscription_plan.services.admin import (
    admin_get_subscription_plan_by_id_service,
)
from apps.user.choices import UserRole
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Subscription Plan"])


@router.get(
    "/{subscription_plan_id}/",
    response=AdminSubscriptionPlanDetailResponse,
    auth=AuthBearer(),
)
def admin_get_subscription_plan_by_id_api(
    request: HttpRequest,
    subscription_plan_id: str = Path(..., description="Subscription Plan ID"),
):
    # Check admin privileges
    if not request.auth or request.auth.role != UserRole.ADMIN:
        return {
            "success": False,
            "message": "Failed to retrieve subscription plan. Insufficient permissions.",
            "errors": [
                {
                    "field": "general",
                    "message": "Only administrators can view subscription plan details",
                }
            ],
            "data": None,
        }

    # Call service to get subscription plan
    subscription_plan, error = admin_get_subscription_plan_by_id_service(
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
            "message": f"Failed to retrieve subscription plan. {status_message}",
            "errors": [{"field": "general", "message": error}],
            "data": None,
        }

    # Success response
    return {
        "success": True,
        "message": "Successfully retrieved subscription plan details",
        "errors": [],
        "data": subscription_plan,
    }
