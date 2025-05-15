from ninja import Schema
from typing import Optional, List
from datetime import datetime

from helpers.dto import PaginationLinks, PaginationMeta, CreatedByInfo


class IndustryCreateRequest(Schema):
    name: str
    description: Optional[str] = None


class IndustryUpdateRequest(Schema):
    name: Optional[str] = None
    description: Optional[str] = None


class IndustryResponse(Schema):
    id: str
    name: str
    description: Optional[str] = None

    # Audit fields
    created_at: datetime
    updated_at: datetime
    created_by: Optional[CreatedByInfo] = None
    updated_by: Optional[CreatedByInfo] = None


class IndustryListResponse(Schema):
    success: bool = True
    message: str
    data: List[IndustryResponse]
    meta: PaginationMeta
    links: PaginationLinks


class IndustryDetailResponse(Schema):
    success: bool
    message: str
    data: Optional[IndustryResponse] = None
