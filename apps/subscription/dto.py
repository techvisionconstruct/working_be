from ninja import Schema
from datetime import datetime
from typing import Optional


class SubscriptionResponse(Schema):
    id: str
    status: str
    subscription_type: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_auto_renew: bool

    # Include basic plan info
    plan_id: Optional[str] = None
    plan_name: Optional[str] = None

    class Config:
        orm_mode = True
