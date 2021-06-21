import os
from typing import List, Union
from pydantic import AnyHttpUrl, BaseSettings, validator
from pathlib import Path


class Settings(BaseSettings):
    BASE_DIR = Path(__file__).resolve().parent.parent
    API_V1_STR: str = os.environ.get('API_V1_STR')
    SECRET_KEY: bytes = os.environ.get('SECRET_KEY')
    PROJECT_NAME: str = os.environ.get('PROJECT_NAME')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    # 60 minutes * 24 hours * 7 days = 7 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.environ.get('BACKEND_CORS_ORIGINS')

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str = os.environ.get('POSTGRES_SERVER')
    POSTGRES_USER: str = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DB: str = os.environ.get('POSTGRES_DB', 'alar')
    SQLALCHEMY_DATABASE_URI: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"

    REDIS_HOST: str = os.environ.get('REDIS_HOST')
    REDIS_PORT: int = os.environ.get('REDIS_PORT')
    REDIS_DB: int = os.environ.get('REDIS_DB')

    class Config:
        case_sensitive = True


settings = Settings()

