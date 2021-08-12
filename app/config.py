from pydantic import BaseSettings


class AppConfig(BaseSettings):
    db_url: str = "postgresql+asyncpg://localhost/fastapi"
    test_db_url: str = "postgresql+asyncpg://localhost/test_fastapi"

    class Config:
        allow_mutation = False
        env_file = ".env"
        env_file_encoding = "utf-8"
