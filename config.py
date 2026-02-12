import os


class Config:
    DATABASE_URL = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:postgres@db:5432/users_db"
    )
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
