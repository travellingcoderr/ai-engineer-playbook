import os

# Port Configuration
# These are read from environment variables passed via docker-compose
PORT_BACKEND = int(os.getenv("PORT", 8080))
PORT_FRONTEND = int(os.getenv("PORT_FRONTEND", 3030))

# Other Constants
DEFAULT_NAMESPACE = "default"
