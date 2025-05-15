import os


environment = os.getenv("ENVIRONMENT", "development")
print('Environment:', environment)
if environment == "development":
    from .dev import *
elif environment == "staging":
    from .staging import *
elif environment == "production":
    from .prod import *
else:
    from .dev import *
