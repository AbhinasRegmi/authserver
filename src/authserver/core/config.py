from typing import List
from functools import lru_cache

from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    CORS_ALLOWED_ORIGINS: List[AnyUrl] = [
        AnyUrl(url="http://localhost:5500", scheme="http"),
        AnyUrl(url="https://abhinasregmi.com.np", scheme="https"),
        AnyUrl(url="https://abhinasregmi.com.np/convert", scheme="https")
    ]

    # jwt constants
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRATION: int = 15  # 15 minutes
    REFRESH_TOKEN_EXPIRATION: int = 7 * 24 * 60  # 7 days
    
    # google api endpoints
    GOOGLE_OAUTH_ROOT_URL: AnyUrl = AnyUrl("https://accounts.google.com/o/oauth2/v2/auth", scheme="https")
    GOOGLE_OAUTH_TOKEN_URL: AnyUrl = AnyUrl("https://oauth2.googleapis.com/token", scheme="https")
    GOOGLE_API_USERINFO_URL: AnyUrl = AnyUrl("https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=", scheme="https")

    GOOGLE_PROFILE_SCOPE_URL: AnyUrl = AnyUrl("https://www.googleapis.com/auth/userinfo.profile", scheme="https")
    GOOGLE_EMAIL_SCOPE_URL: AnyUrl = AnyUrl("https://www.googleapis.com/auth/userinfo.email", scheme="https")

    # -------------- .env --------------------

    # internal api endpoints
    AUTHSERVER_GOOGLE_CALLBACK_URL: AnyUrl
    AUTHSERVER_USER_DETAIL_PATH: AnyUrl

    # google keys 
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # jwt secrets
    JWT_ACCESS_SECRET: str
    JWT_REFRESH_SECRET: str

    # db connection uris
    POSTGRESQL_DB_URI: str



@lru_cache(maxsize=128)
def setting() -> Settings:
    return Settings() #type:ignore


settings = setting()