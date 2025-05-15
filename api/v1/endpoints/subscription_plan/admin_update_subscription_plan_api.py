from ninja import Router, Path
from django.http import HttpRequest
from ninja.responses import Response

from apps.subscription_plan.dto import (
    AdminUpdateSubscriptionPlanRequest,
    AdminUpdateSubscriptionPlanResponse,
)
from apps.subscription_plan.services.admin.admin_update_subscription_plan_service import (
    admin_update_subscription_plan_service,
)
from apps.user.choices import UserRole
from apps.auth.services.authenticate_service import AuthBearer

router = Router(tags=["Subscription Plan"])


@router.put(
    "/{subscription_plan_id}/",
    response={
        200: AdminUpdateSubscriptionPlanResponse,
        400: AdminUpdateSubscriptionPlanResponse,
        403: AdminUpdateSubscriptionPlanResponse,
    },
    auth=AuthBearer(),
)
def admin_update_subscription_plan_api(
    request: HttpRequest,
    payload: AdminUpdateSubscriptionPlanRequest,
    subscription_plan_id: str = Path(..., description="Subscription Plan ID"),
):
    if not request.auth or request.auth.role != UserRole.ADMIN:
        return Response(
            {
                "success": False,
                "message": "Failed to update subscription plan. Insufficient permissions.",
                "errors": [
                    {
                        "field": "general",
                        "message": "Only administrators can update subscription plans",
                    }
                ],
                "data": None,
            },
            status=403,
        )

    plan_data, error = admin_update_subscription_plan_service(
        admin_user=request.auth,
        subscription_plan_id=subscription_plan_id,
        name=payload.name,
        description=payload.description,
        price=payload.price,
        period=payload.period,
        duration_days=payload.duration_days,
        is_active=payload.is_active,
    )

    if error:
        field_errors = []
        if "Permission denied" in error:
            field_errors.append(
                {"field": "general", "message": "Insufficient permissions"}
            )
            formatted_error = (
                "Failed to update subscription plan. Insufficient permissions."
            )
            status_code = 403
        else:
            field_errors.append({"field": "general", "message": error})
            formatted_error = f"Failed to update subscription plan. {error}"
            status_code = 400

        return Response(
            {
                "success": False,
                "message": formatted_error,
                "errors": field_errors,
                "data": None,
            },
            status=status_code,
        )

    return Response(
        {
            "success": True,
            "message": "Successfully updated subscription plan",
            "errors": [],
            "data": plan_data,
        },
        status=200,
    )
