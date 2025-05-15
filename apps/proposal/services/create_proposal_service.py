from typing import Optional, Tuple
from apps.template.dto import TemplateCreateRequest
from apps.proposal.models import Proposal
from apps.proposal.dto import ProposalCreateRequest
from apps.template.models import Template
from apps.template.choices import TemplateOrigin
from apps.trade.models import Trade
from apps.variable.models import Variable
from apps.user.models import User
from helpers.process_base64_image import process_base64_image
from helpers.create_derived_template import create_derived_template
from helpers.create_derived_trade import create_derived_trade
from helpers.create_derived_variable import create_derived_variable


def create_proposal_service(
    payload: ProposalCreateRequest, user: User
) -> Tuple[Optional[Proposal], Optional[str]]:
    print(payload.template)
    try:
        # Process image if provided
        image_file = None
        if payload.image:
            try:
                image_file = process_base64_image(payload.image)
            except Exception as e:
                return None, f"Error processing image: {str(e)}"

        # Handle template if provided
        template = None
        if payload.template:
            try:
                source_template = Template.objects.get(id=payload.template)
                template = create_derived_template(source_template, user)
            except Template.DoesNotExist:
                return None, f"Template with ID {payload.template} does not exist."
            except Exception as e:
                return None, f"Error creating derived template: {str(e)}"
        else:
            try:
                template = Template.objects.create(
                    name=f"{payload.name} Template",
                    description=f"Template created for proposal: {payload.name}",
                    status="draft",
                    origin=TemplateOrigin.DERIVED,
                    owner=user,
                    is_public=False,
                    created_by=user,
                    updated_by=user,
                )

            except Exception as e:
                return None, f"Error creating new template: {str(e)}"

        proposal = Proposal(
            name=payload.name,
            description=payload.description,
            status=payload.status,
            image=image_file,
            template=template,
            owner=user,
            client_name=payload.client_name,
            client_email=payload.client_email,
            client_phone=payload.client_phone,
            client_address=payload.client_address,
            valid_until=payload.valid_until,
            created_by=user,
            updated_by=user,
        )

        proposal.save()
        return proposal, None
    except Exception as e:
        return None, f"Error creating proposal: {str(e)}"
