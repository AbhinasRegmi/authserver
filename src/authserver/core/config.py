from functools import lru_cache

from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    
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



@lru_cache(maxsize=128)
def setting() -> Settings:
    return Settings() #type:ignore


settings = setting()