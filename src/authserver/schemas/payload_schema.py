from pydantic import BaseSettings, EmailStr, AnyHttpUrl, Field


class JWTPayload(BaseSettings):
    email: EmailStr = Field(...)
    avatar: AnyHttpUrl = Field(...)


class GoogleResponsePayload(JWTPayload):
    verified: bool = Field(default=True)