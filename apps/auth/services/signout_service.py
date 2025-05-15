from apps.jwt.services import delete_token_service


def signout_service(user, access_token):
    # Delete the token
    try:
        delete_token_service(user, access_token)
        return None
    except Exception as e:
        return str(e)
