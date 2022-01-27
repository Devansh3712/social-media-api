from pydantic import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"

settings = Settings()
