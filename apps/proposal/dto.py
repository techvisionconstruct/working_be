from ninja import Schema
from typing import Optional, List
from datetime import datetime
from apps.user.dto import UserResponse
from helpers.dto import PaginationLinks, PaginationMeta, CreatedByInfo
from apps.template.dto import TemplateResponse, TemplateCreateRequest
from apps.contract.dto import ContractResponse


class ProposalResponse(Schema):
    id: str
    name: str
    description: Optional[str] = None
    status: str
    image: Optional[str] = None
    template: Optional[TemplateResponse] = None
    contract: Optional[ContractResponse] = None
    owner: Optional[UserResponse] = None
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    valid_until: Optional[datetime] = None
    total_material_cost: Optional[float] = None
    total_labor_cost: Optional[float] = None
    total_with_markup: Optional[float] = None
    total_cost: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[CreatedByInfo] = None
    updated_by: Optional[CreatedByInfo] = None


class ProposalListResponse(Schema):
    success: bool
    message: str
    data: List[ProposalResponse]
    links: PaginationLinks
    meta: PaginationMeta


class ProposalDetailResponse(Schema):
    success: bool
    message: str
    data: Optional[ProposalResponse]


class ProposalCreateRequest(Schema):
    name: str
    description: Optional[str] = None
    status: Optional[str] = None
    image: Optional[str] = None
    template: Optional[str] = None
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    valid_until: Optional[datetime] = None


class ProposalUpdateRequest(Schema):
    name: str
    description: Optional[str] = None
    status: Optional[str] = None
    image: Optional[str] = None
    template: Optional[str] = None
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    valid_until: Optional[datetime] = None


class ErrorResponseSchema(Schema):
    error: str


class SendProposalRequest(Schema):
    proposal_id: str
