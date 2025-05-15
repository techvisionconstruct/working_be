# filepath: /Users/naigggs/Documents/Projects/service/apps/user_profile/dto.py
from ninja import Schema
from typing import Optional, List
from datetime import datetime
from apps.industry.dto import IndustryResponse

from helpers.dto import PaginationLinks, PaginationMeta, CreatedByInfo


class ProfileResponse(Schema):
    id: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

    # Contact Information
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

    # Professional Information
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    industry: Optional[IndustryResponse] = None
    years_of_experience: Optional[int] = None

    # Audit fields
    created_by: CreatedByInfo
    updated_by: CreatedByInfo
    created_at: datetime
    updated_at: datetime


class ProfileListResponse(Schema):
    success: bool
    message: str
    data: List[ProfileResponse]
    meta: PaginationMeta
    links: PaginationLinks


class ProfileDetailResponse(Schema):
    success: bool
    message: str
    data: Optional[ProfileResponse] = None


class ProfileCreateRequest(Schema):
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

    # Contact Information
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

    # Professional Information
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    industry_id: Optional[str] = None
    years_of_experience: Optional[int] = None


class ProfileUpdateRequest(Schema):
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

    # Contact Information
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

    # Professional Information
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    industry_id: Optional[str] = None
    years_of_experience: Optional[int] = None
