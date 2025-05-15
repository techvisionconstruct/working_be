def format_signin_error(error: str) -> str:
    # Common error mappings
    error_mappings = {
        "Invalid credentials": "Failed to authenticate user. Invalid email or password.",
        "User account is disabled": "Failed to authenticate user. Account is disabled.",
        "User account is blocked": "Failed to authenticate user. Account is blocked.",
        "User account is suspended": "Failed to authenticate user. Account is suspended.",
        "Email is required": "Failed to authenticate user. Email is required.",
        "Password is required": "Failed to authenticate user. Password is required.",
        "Invalid email format": "Failed to authenticate user. Email format is invalid.",
    }

    # Return mapped error or fallback to generic format
    return error_mappings.get(error, f"Failed to authenticate user. {error}")
