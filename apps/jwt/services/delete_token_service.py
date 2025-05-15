from apps.jwt.models import JWTToken


def delete_token_service(user, access_token):
    # Delete the token
    try:
        token = JWTToken.objects.get(user=user, access_token=access_token)
        token.delete()
        return True
    except JWTToken.DoesNotExist:
        return False
