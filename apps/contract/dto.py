from ninja import Schema
from typing import Optional, List
from datetime import datetime
from apps.user.dto import UserResponse
from helpers.dto import PaginationLinks, PaginationMeta, CreatedByInfo


class ContractResponse(Schema):
    id: str
    name: str
    description: Optional[str] = None
    status: str
    terms: Optional[str] = None

    # Signature fields
    client_initials: Optional[str] = None
    client_signature: Optional[str] = None
    client_signed_at: Optional[datetime] = None

    contractor_initials: Optional[str] = None
    contractor_signature: Optional[str] = None
    contractor_signed_at: Optional[datetime] = None

    # Relationships
    owner: Optional[UserResponse] = None

    # Audit fields
    created_at: datetime
    updated_at: datetime
    created_by: Optional[CreatedByInfo] = None
    updated_by: Optional[CreatedByInfo] = None


class ContractListResponse(Schema):
    success: bool
    message: str
    data: List[ContractResponse]
    links: PaginationLinks
    meta: PaginationMeta


class ContractDetailResponse(Schema):
    success: bool
    message: str
    data: Optional[ContractResponse]


class ContractCreateRequest(Schema):
    name: str
    description: Optional[str] = None
    contractor_initials: Optional[str] = None
    contractor_signature: Optional[str] = None
    status: Optional[str] = None
    terms: Optional[str] = None
    proposal_id: str


class ContractUpdateRequest(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    contractor_initials: Optional[str] = None
    contractor_signature: Optional[str] = None
    status: Optional[str] = None
    terms: Optional[str] = None


class ContractSignRequest(Schema):
    client_initials: Optional[str] = None
    client_signature: Optional[str] = None
