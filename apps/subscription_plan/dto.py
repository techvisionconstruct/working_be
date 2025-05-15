from ninja import Schema
from typing import Optional, List, Dict
from datetime import datetime

from helpers.dto import ErrorItem


class CreatedByInfo(Schema):
    id: str
    email: str
    username: Optional[str]
    first_name: str
    last_name: str
    role: str


class AdminSubscriptionPlanItem(Schema):
    id: str
    name: str
    description: Optional[str]
    price: float
    period: str
    duration_days: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[CreatedByInfo] = None


class AdminSubscriptionPlanListResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    data: List[AdminSubscriptionPlanItem] = []
    links: Dict = {}
    meta: Dict = {}


class AdminSubscriptionPlanDetailResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    data: Optional[AdminSubscriptionPlanItem] = None


class AdminCreateSubscriptionPlanRequest(Schema):
    name: str
    description: Optional[str] = None
    price: float
    period: str
    duration_days: int
    is_active: bool = True


class AdminCreateSubscriptionPlanResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    data: Optional[AdminSubscriptionPlanItem] = None


class AdminUpdateSubscriptionPlanRequest(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    period: Optional[str] = None
    duration_days: Optional[int] = None
    is_active: Optional[bool] = None


class AdminUpdateSubscriptionPlanResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    data: Optional[AdminSubscriptionPlanItem] = None


class AdminDeleteSubscriptionPlanResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    data: None = None
