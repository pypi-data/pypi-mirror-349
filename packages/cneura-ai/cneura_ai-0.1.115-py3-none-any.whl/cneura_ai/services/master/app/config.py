from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_HOST: str
    MONGO_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str = None

    SQLITE_PATH: str

    CHROMADB_HOST: str
    CHROMADB_PORT: int
    CHROMADB_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
