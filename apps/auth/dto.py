from typing import Optional, List
from ninja import Schema

from apps.user.dto import UserResponse


class ErrorItem(Schema):
    field: str
    message: str


class SignInRequest(Schema):
    email: str
    password: str


class SignUpRequest(Schema):
    email: str
    password: str
    first_name: str
    last_name: str
    username: Optional[str] = None


class TokenResponse(Schema):
    token_type: str
    access_token: str
    refresh_token: str
    access_token_expires_at: str
    refresh_token_expires_at: str


class SignInResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    user: Optional[UserResponse] = None
    tokens: Optional[TokenResponse] = None


class SignUpResponse(Schema):
    success: bool
    message: str
    user: UserResponse


class SignOutResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []


class RefreshTokenRequest(Schema):
    refresh_token: str


class RefreshTokenResponse(Schema):
    success: bool
    message: str
    errors: List[ErrorItem] = []
    tokens: Optional[TokenResponse] = None
