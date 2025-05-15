from typing import Optional, Tuple

from apps.template.models import Template
from apps.user.models import User
from apps.trade.models import Trade
from apps.variable.models import Variable
from helpers.process_base64_image import process_base64_image


def update_proposal_template_service(
    template_id: str, payload: dict, user: User
) -> Tuple[Optional[Template], Optional[str]]:
    try:
        # Check if the template exists
        try:
            template = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return None, f"Template with ID {template_id} not found."

        # Check permissions
        if template.created_by != user and (
            template.owner != user and user.is_staff is not True
        ):
            return None, "You don't have permission to update this template."

        # Process image if provided
        if "image" in payload:
            image = payload["image"]
            if image:
                try:
                    image_file = process_base64_image(image)
                    template.image = image_file
                except Exception as e:
                    return None, f"Error processing image: {str(e)}"
            else:
                # If empty string or null is provided, clear the image
                template.image = None

        # Update basic fields if provided
        if "name" in payload:
            template.name = payload["name"]

        if "description" in payload:
            template.description = payload["description"]

        if "status" in payload:
            template.status = payload["status"]

        if "is_public" in payload:
            template.is_public = payload["is_public"]

        # Update source_id if provided (only if template is 'derived')
        if "source_id" in payload and template.origin == "derived":
            try:
                source_template = Template.objects.get(id=payload["source_id"])

                # Check if user has access to the source template
                if not source_template.is_public and source_template.created_by != user:
                    return (
                        None,
                        "You don't have permission to use this template as a source.",
                    )

                template.source_id = source_template
            except Template.DoesNotExist:
                return (
                    None,
                    f"Source template with ID {payload['source_id']} not found.",
                )

        # Add trades if provided
        if "trades" in payload:
            # Clear existing trades and add new ones
            template.trades.clear()
            if payload["trades"]:
                trade_objects = Trade.objects.filter(id__in=payload["trades"])
                template.trades.add(*trade_objects)

        # Add variables if provided
        if "variables" in payload:
            # Clear existing variables and add new ones
            template.variables.clear()
            if payload["variables"]:
                variable_objects = Variable.objects.filter(id__in=payload["variables"])
                template.variables.add(*variable_objects)

        template.owner = user

        # Update audit information
        template.updated_by = user

        # Save changes
        template.save()

        return template, None
    except Exception as e:
        return None, f"Error updating template: {str(e)}"
