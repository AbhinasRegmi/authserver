from pydantic import BaseSettings, EmailStr, AnyHttpUrl, Field


class ResponsePayload(BaseSettings):
    username: str = Field(...)
    email: EmailStr = Field(...)
    avatar: AnyHttpUrl = Field(...)


class GoogleResponsePayload(ResponsePayload):
    valid: bool = Field(default=False)