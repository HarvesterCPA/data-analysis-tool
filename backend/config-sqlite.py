# SQLite configuration for development
# Use this instead of PostgreSQL for easier setup

DATABASE_URL = "sqlite:///./harvester_tracking.db"
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALLOWED_ORIGINS = ["http://localhost:3000"]
