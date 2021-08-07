from pydantic import BaseSettings


class Settings(BaseSettings):

    INFLUXDB_URL: str
    INFLUXDB_TOKEN: str
    INFLUXDB_ORG: str
    INFLUXDB_BUCKET: str

    TIMEOUT_IN_SEC: int = 60*15  # 15 minutes

    class Config:
        case_sensitive = True


settings = Settings()
