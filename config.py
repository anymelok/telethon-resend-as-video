from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    API_ID: int
    API_HASH: str
    MY_ID: int

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
