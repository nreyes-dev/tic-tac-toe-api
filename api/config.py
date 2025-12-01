from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    python_env: str = "development"  # "development" or "production"
    deployed_front_domain: str = ""
    logging_lvl: str = "info"
    api_port: int = 8080

    # extra="allow" allows other .env vars not listed here
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
