from pydantic_settings import BaseSettings
from pydantic import AnyUrl, EmailStr

from typing import List

class AppSettings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    
    root_path: str = "/api/v1"
    cors_allowed: List[str] = ["*"]
    environment: str

    db_connection_url: str
    database_name: str
    unique_collection: str
    profit_collection: str


    username: str
    email: EmailStr
    password: str

    class Config:
        env_file = ".env"  # Load values from .env file

app_config = AppSettings()