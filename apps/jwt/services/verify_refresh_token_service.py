import jwt
from typing import Dict, Optional
from config.constants import JWT_CONFIG, ENVIRONMENT


def verify_refresh_token_service(refresh_token: str) -> Optional[Dict]:
    try:
        # Get the correct refresh secret from JWT configuration
        env = ENVIRONMENT or "development"
        jwt_config = JWT_CONFIG.get(env, JWT_CONFIG["development"])
        refresh_secret = jwt_config["REFRESH_SECRET"]

        # Decode the token with the correct secret
        payload = jwt.decode(refresh_token, refresh_secret, algorithms=["HS256"])

        # Check if it's a refresh token
        if payload.get("type") != "refresh":
            return None

        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None
