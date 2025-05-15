# filepath: /Users/naigggs/Documents/Projects/service/apps/variable_type/dto.py
from ninja import Schema
from typing import Optional, List
from datetime import datetime

from helpers.dto import PaginationLinks, PaginationMeta, CreatedByInfo


class VariableTypeResponse(Schema):
    id: str
    name: str
    description: Optional[str] = None
    category: str
    unit: Optional[str] = None
    is_built_in: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[CreatedByInfo] = None
    updated_by: Optional[CreatedByInfo] = None


class VariableTypeListResponse(Schema):
    success: bool
    message: str
    data: List[VariableTypeResponse]
    links: PaginationLinks
    meta: PaginationMeta


class VariableTypeDetailResponse(Schema):
    success: bool
    message: str
    data: Optional[VariableTypeResponse]


class VariableTypeCreateRequest(Schema):
    name: str
    description: Optional[str] = None
    category: str
    unit: Optional[str] = None
    is_built_in: Optional[bool] = False


class VariableTypeUpdateRequest(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    is_built_in: Optional[bool] = None
