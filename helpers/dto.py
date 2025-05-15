from ninja import Schema
from typing import Optional


class ErrorItem(Schema):
    field: str
    message: str


class PaginationLinks(Schema):
    self: str
    first: str
    last: str
    next: Optional[str] = None
    prev: Optional[str] = None


class PaginationMeta(Schema):
    current_page: int
    total_pages: int
    page_size: int
    total_count: int


class CreatedByInfo(Schema):
    id: str
    email: str
    username: Optional[str]
    first_name: str
    last_name: str
