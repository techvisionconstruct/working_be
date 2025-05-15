import jwt
import datetime
from typing import Tuple

from apps.user.models import User
from helpers import parse_expiry_time_service
from config.constants import JWT_CONFIG, ENVIRONMENT


def generate_tokens_service(
    user: User,
) -> Tuple[str, str, datetime.datetime, datetime.datetime]:
    environment = ENVIRONMENT or "development"
    jwt_config = JWT_CONFIG.get(environment, JWT_CONFIG["development"])

    access_secret = jwt_config["ACCESS_SECRET"]
    refresh_secret = jwt_config["REFRESH_SECRET"]
    access_expires_in = jwt_config["ACCESS_EXPIRES_IN"] or "1d"
    refresh_expires_in = jwt_config["REFRESH_EXPIRES_IN"] or "7d"

    # Parse expiration times
    access_expiry = parse_expiry_time_service(access_expires_in)
    refresh_expiry = parse_expiry_time_service(refresh_expires_in)

    # Create timestamps
    access_expires_at = datetime.datetime.now(datetime.timezone.utc) + access_expiry
    refresh_expires_at = datetime.datetime.now(datetime.timezone.utc) + refresh_expiry

    # Create the JWT tokens
    access_payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": access_expires_at,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "type": "access",
    }

    refresh_payload = {
        "user_id": user.id,
        "exp": refresh_expires_at,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "type": "refresh",
    }

    access_token = jwt.encode(access_payload, access_secret, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, refresh_secret, algorithm="HS256")

    return access_token, refresh_token, access_expires_at, refresh_expires_at
