from .create_proposal_service import create_proposal_service
from .get_all_proposals_service import get_all_proposals_service
from .get_proposal_by_id_service import get_proposal_by_id_service
from .delete_proposal_service import delete_proposal_service
from .update_proposal_service import update_proposal_service
from .send_proposal_to_client_service import send_proposal_to_client_service
from .update_proposal_template_service import update_proposal_template_service


all = {
    "create_proposal_service",
    "get_all_proposals_service",
    "get_proposal_by_id_service",
    "delete_proposal_service",
    "update_proposal_service",
    "send_proposal_to_client_service",
    "update_proposal_template_service",
}
