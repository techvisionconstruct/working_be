# filepath: /Users/naigggs/Documents/Projects/service/apps/trade/dto.py
from ninja import Schema
from typing import Optional, List
from datetime import datetime

from helpers.dto import PaginationLinks, PaginationMeta, CreatedByInfo
from apps.element.dto import ElementResponse


class TradeResponse(Schema):
    id: str
    name: str
    description: Optional[str] = None
    elements: Optional[List[ElementResponse]] = None
    origin: str
    created_at: datetime
    updated_at: datetime
    created_by: Optional[CreatedByInfo] = None
    updated_by: Optional[CreatedByInfo] = None


class TradeListResponse(Schema):
    success: bool
    message: str
    data: List[TradeResponse]
    links: PaginationLinks
    meta: PaginationMeta


class TradeDetailResponse(Schema):
    success: bool
    message: str
    data: Optional[TradeResponse]


class TradeCreateRequest(Schema):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    elements: Optional[List[str]] = None


class TradeUpdateRequest(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    elements: Optional[List[str]] = None
