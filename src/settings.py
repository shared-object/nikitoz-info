from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_id: int
    app_hash: str
    nikitoz_address: str
    chat_id: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


def load_settings(env_file=".env") -> Settings:
    config = Settings(_env_file=env_file) # type: ignore
    return config
