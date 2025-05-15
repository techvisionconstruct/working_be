from apps.user.models import User


def update_signin_status_service(user: User, is_sign_in: bool = True) -> User:
    user.is_sign_in = is_sign_in
    user.save(update_fields=["is_sign_in"])
    return user
