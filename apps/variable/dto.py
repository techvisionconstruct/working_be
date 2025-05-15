from ninja import Schema
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from helpers.dto import PaginationLinks, PaginationMeta, CreatedByInfo
from apps.variable_type.dto import VariableTypeResponse


class VariableResponse(Schema):
    id: str
    name: str
    description: Optional[str] = None
    formula: Optional[str] = None
    value: Optional[Decimal] = None
    origin: str
    is_global: bool
    variable_type: Optional[VariableTypeResponse] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[CreatedByInfo] = None
    updated_by: Optional[CreatedByInfo] = None


class VariableListResponse(Schema):
    success: bool
    message: str
    data: List[VariableResponse]
    links: PaginationLinks
    meta: PaginationMeta


class VariableDetailResponse(Schema):
    success: bool
    message: str
    data: Optional[VariableResponse]


class VariableCreateRequest(Schema):
    name: str
    description: Optional[str] = None
    formula: Optional[str] = None
    value: Optional[Decimal] = None
    is_global: Optional[bool] = False
    variable_type: Optional[str] = None


class VariableUpdateRequest(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    formula: Optional[str] = None
    value: Optional[Decimal] = None
    is_global: Optional[bool] = None
    variable_type: Optional[str] = None
