from typing import Optional, List
from ninja import Schema


class VerifyOTPRequest(Schema):
    email: str
    otp_code: str
    password: str
    first_name: str
    last_name: str
