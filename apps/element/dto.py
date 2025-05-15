from ninja import Schema
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

from helpers.dto import PaginationLinks, PaginationMeta, CreatedByInfo

from apps.user.dto import UserResponse


class ElementResponse(Schema):
    id: str
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    origin: str
    material_cost_formula: Optional[str] = None
    material_formula_variables: Optional[List[Dict[str, Any]]] = None
    labor_cost_formula: Optional[str] = None
    labor_formula_variables: Optional[List[Dict[str, Any]]] = None
    material_cost: Optional[Decimal] = None
    labor_cost: Optional[Decimal] = None
    markup: Optional[Decimal] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[CreatedByInfo] = None
    updated_by: Optional[CreatedByInfo] = None


class ElementListResponse(Schema):
    success: bool
    message: str
    data: List[ElementResponse]
    links: PaginationLinks
    meta: PaginationMeta


class ElementDetailResponse(Schema):
    success: bool
    message: str
    data: Optional[ElementResponse]


class ElementCreateRequest(Schema):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    material_cost_formula: Optional[str] = None
    labor_cost_formula: Optional[str] = None
    markup: Optional[Decimal] = None


class ElementUpdateRequest(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    material_cost_formula: Optional[str] = None
    labor_cost_formula: Optional[str] = None
    markup: Optional[Decimal] = None
