from typing import Optional, Tuple
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.proposal.models import Proposal
from apps.proposal.dto import SendProposalRequest

def send_proposal_to_client_service(
    payload: SendProposalRequest,
    context: Optional[dict] = None
) -> Tuple[bool, Optional[str]]:
    try:
        proposal = Proposal.objects.get(id=payload.proposal_id)
        subject = f"Your Proposal {proposal.name} is Ready"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [proposal.client_email]

        # Prepare context for email template
        message_data = {
            "client_email": proposal.client_email,
            "proposal": proposal,
        }
        if context:
            message_data.update(context)

        html_message = render_to_string('./email.html', message_data)
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            from_email,
            recipient_list,
            html_message=html_message
        )
        return True, None
    except Exception as e:
        return False, str(e)