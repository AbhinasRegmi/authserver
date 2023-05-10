from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        case_sensitive = True



@lru_cache(maxsize=128)
def setting() -> Settings:
    return Settings() #type:ignore