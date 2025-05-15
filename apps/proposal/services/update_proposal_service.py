from typing import Optional, Tuple
from apps.proposal.models import Proposal
from apps.user.models import User
from helpers.process_base64_image import process_base64_image


def update_proposal_service(
    proposal_id: str,
    payload: dict,
    user: User,
) -> Tuple[Optional[Proposal], Optional[str]]:
    try:
        # Check if the proposal exists
        try:
            proposal = Proposal.objects.get(id=proposal_id)
        except Proposal.DoesNotExist:
            return None, f"Proposal with ID {proposal_id} not found."

        # Check if user has permission
        if proposal.created_by != user and not user.is_staff:
            return None, "You don't have permission to update this proposal."

        # Handle image if present as base64 string
        if "image" in payload:
            image = payload.pop("image")
            if image:
                try:
                    image_file = process_base64_image(image)
                    proposal.image = image_file
                except Exception as e:
                    return None, f"Error processing image: {str(e)}"

        # Update fields if provided in payload
        if "name" in payload:
            proposal.name = payload["name"]

        if "description" in payload:
            proposal.description = payload["description"]

        if "status" in payload:
            proposal.status = payload["status"]

        if "template" in payload:
            proposal.template = payload["template"]

        if "client_name" in payload:
            proposal.client_name = payload["client_name"]

        if "client_email" in payload:
            proposal.client_email = payload["client_email"]

        if "client_phone" in payload:
            proposal.client_phone = payload["client_phone"]

        if "client_address" in payload:
            proposal.client_address = payload["client_address"]

        proposal.owner = user
        # Update the audit field
        proposal.updated_by = user
        proposal.save()
        return proposal, None
    except Exception as e:
        return None, f"Error updating proposal: {str(e)}"
