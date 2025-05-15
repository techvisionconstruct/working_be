from ninja import Schema
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

from helpers.dto import PaginationLinks, PaginationMeta
from apps.user.dto import UserResponse, ErrorItem


class ProductResponse(Schema):
    id: str
    search_term: str
    source_platform: str
    title: Optional[str] = None
    item_id: Optional[str] = None
    link: Optional[str] = None
    primary_image: Optional[str] = None
    rating: Optional[Decimal] = None
    ratings_total: Optional[int] = None
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UserResponse] = None
    updated_by: Optional[UserResponse] = None


class ProductListResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    data: List[ProductResponse]
    links: PaginationLinks
    meta: PaginationMeta


class ProductDetailResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    data: Optional[ProductResponse]


class ProductSearchRequest(Schema):
    search_term: str
    sort_by: Optional[str] = "price_low_to_high"


class HomeDepotProductSearchResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    data: List[ProductResponse]
    links: PaginationLinks
    meta: PaginationMeta
