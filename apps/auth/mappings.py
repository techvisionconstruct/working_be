SIGNIN_ERROR_MAPPINGS = {
    r"Invalid credentials": ["email", "password"],
    r"Invalid email format": "email",
    r"Email is required": "email",
    r"Password is required": "password",
    r"User account is disabled": "general",
    r"User account is blocked": "general",
    r"User account is suspended": "general",
    r"Error generating authentication tokens": "general",
    r"Error saving authentication tokens": "general",
}

# Add these if not already present
SIGNUP_ERROR_MAPPINGS = {
    r"Email is required": "email",
    r"Invalid email format": "email",
    r"Email already exists": "email",
    r"Username is required": "username",
    r"Username already exists": "username",
    r"Password is required": "password",
    r"Password must be at least": "password",
    r"First name is required": "first_name",
    r"Last name is required": "last_name",
}
