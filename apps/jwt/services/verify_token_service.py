import jwt
from typing import Dict

from config.constants import JWT_CONFIG, ENVIRONMENT


def verify_token_service(token: str, token_type: str = "access") -> Dict:
    env = ENVIRONMENT or "development"
    jwt_config = JWT_CONFIG.get(env, JWT_CONFIG["development"])
    if token_type == "access":
        secret = jwt_config["ACCESS_SECRET"]
    else:
        secret = jwt_config["REFRESH_SECRET"]

    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
