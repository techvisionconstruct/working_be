from ninja import Schema
from typing import Optional, List
from datetime import datetime

from helpers.dto import PaginationLinks, PaginationMeta, CreatedByInfo

from apps.trade.dto import TradeResponse
from apps.variable.dto import VariableResponse
from apps.user.dto import UserResponse


class TemplateResponse(Schema):
    id: str
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    trades: Optional[List[TradeResponse]] = None
    variables: Optional[List[VariableResponse]] = None
    status: str
    origin: str
    is_public: bool
    owner: Optional[UserResponse] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[CreatedByInfo] = None
    updated_by: Optional[CreatedByInfo] = None


class TemplateListResponse(Schema):
    success: bool
    message: str
    data: List[TemplateResponse]
    links: PaginationLinks
    meta: PaginationMeta


class TemplateDetailResponse(Schema):
    success: bool
    message: str
    data: Optional[TemplateResponse]


class TemplateCreateRequest(Schema):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    status: Optional[str] = "draft"
    origin: Optional[str] = "original"
    is_public: Optional[bool] = None
    source_id: Optional[str] = None
    trades: Optional[List[str]] = None
    variables: Optional[List[str]] = None
    is_public: Optional[bool] = False


class TemplateUpdateRequest(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    status: Optional[str] = None
    is_public: Optional[bool] = None
    source_id: Optional[str] = None
    trades: Optional[List[str]] = None
    variables: Optional[List[str]] = None
