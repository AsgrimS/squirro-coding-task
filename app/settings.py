from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_db: str
    mongo_username: str
    mongo_password: str

    class Config:
        env_file = ".env"


settings = Settings()
