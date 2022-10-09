from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_db: str
    mongo_username: str
    mongo_password: str

    summarization_cache_timeout: int = 60 * 10  # 10 minutes

    class Config:
        env_file = ".env"


settings = Settings()
