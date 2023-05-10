from pydantic import BaseModel, Field


class ResponseToken(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)
    token_type: str = "Bearer"

    class Config:
        frozen = True