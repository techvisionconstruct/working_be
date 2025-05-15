import random
import string
from datetime import datetime, timedelta


def generate_otp(length=6):
    # Generate random digits
    otp = "".join(random.choices(string.digits, k=length))
    return otp


def get_otp_expiry_time(minutes=10):
    return datetime.now() + timedelta(minutes=minutes)
