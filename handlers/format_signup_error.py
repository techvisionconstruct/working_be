def format_signup_error(error: str) -> str:
    # Common error mappings
    error_mappings = {
        "Email is required": "Failed to register user. Email is required.",
        "Invalid email format": "Failed to register user. Invalid email format.",
        "Email already exists": "Failed to register user. Email is already registered.",
        "Username is required": "Failed to register user. Username is required.",
        "Username already exists": "Failed to register user. Username is already taken.",
        "Password is required": "Failed to register user. Password is required.",
        "Password must be at least 8 characters": "Failed to register user. Password must be at least 8 characters.",
        "First name is required": "Failed to register user. First name is required.",
        "Last name is required": "Failed to register user. Last name is required.",
    }

    # Return mapped error or fallback to generic format
    return error_mappings.get(error, f"Failed to register user. {error}")
