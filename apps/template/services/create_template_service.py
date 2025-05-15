from typing import Optional, Tuple, List

from apps.template.models import Template
from apps.user.models import User
from apps.template.dto import TemplateCreateRequest
from apps.trade.models import Trade
from apps.variable.models import Variable
from helpers.process_base64_image import process_base64_image
from helpers.create_derived_variable import create_derived_variable
from helpers.create_derived_trade import create_derived_trade


def create_template_service(
    payload: TemplateCreateRequest, user: User
) -> Tuple[Optional[Template], Optional[str]]:
    try:
        # Check if source template exists if derived
        source_template = None
        if payload.origin == "derived" and payload.source_id:
            try:
                source_template = Template.objects.get(id=payload.source_id)

                # Check if user has access to the source template
                if not source_template.is_public and source_template.created_by != user:
                    return (
                        None,
                        "You don't have permission to use this template as a source.",
                    )
            except Template.DoesNotExist:
                return None, f"Source template with ID {payload.source_id} not found."

        # Process image if provided
        image_file = None
        if payload.image:
            try:
                image_file = process_base64_image(payload.image)
            except Exception as e:
                return None, f"Error processing image: {str(e)}"

        # Create the template
        template = Template(
            # Template Details
            name=payload.name,
            description=payload.description,
            image=image_file,
            status=payload.status,
            source_id=source_template,
            is_public=False,
            owner=user,
            # Audit
            created_by=user,
            updated_by=user,
        )
        template.save()

        return template, None
    except Exception as e:
        return None, f"Error creating template: {str(e)}"
