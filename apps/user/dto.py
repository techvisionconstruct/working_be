from ninja import Schema
from typing import Optional, List, Dict
from datetime import datetime

from helpers.dto import PaginationLinks, PaginationMeta
from apps.subscription.dto import SubscriptionResponse


class ErrorItem(Schema):
    field: str
    message: str


class UserResponse(Schema):
    id: str
    email: str
    username: str
    first_name: str
    last_name: str
    role: str
    is_superuser: bool
    is_staff: bool
    is_active: bool
    subscription: Optional[SubscriptionResponse] = None


# Admin Create User DTOs
class AdminCreateUserRequest(Schema):
    email: str
    password: str
    first_name: str
    last_name: str
    username: Optional[str] = None
    role: str = "user"
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False


class AdminCreateUserResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    user: Optional[UserResponse] = None


# Admin Update User DTOs
class AdminUpdateUserRequest(Schema):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    is_staff: Optional[bool] = None
    is_superuser: Optional[bool] = None
    password: Optional[str] = None


class CreatedByInfo(Schema):
    id: str
    email: str
    username: Optional[str]
    first_name: str
    last_name: str
    role: str


class AdminUserListItem(Schema):
    id: str
    email: str
    username: Optional[str]
    first_name: str
    last_name: str
    role: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[CreatedByInfo] = None


# Admin List Users DTO
class AdminUserListResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    data: List[AdminUserListItem] = []
    links: PaginationLinks
    meta: PaginationMeta


# Admin Get User Detail DTO
class AdminUserDetailResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    data: Optional[AdminUserListItem] = None


# Admin Delete User DTO
class AdminUserDeleteResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    data: None = None
