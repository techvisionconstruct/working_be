def determine_status_code(error: str) -> int:
    """Determine appropriate HTTP status code based on error message"""

    if any(
        term in error.lower()
        for term in ["invalid credentials", "password", "email format"]
    ):
        return 401  # Unauthorized

    if any(term in error.lower() for term in ["disabled", "blocked", "suspended"]):
        return 403  # Forbidden

    if "required" in error.lower():
        return 400  # Bad Request

    return 401
