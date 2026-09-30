from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    db_user: str
    db_password: str
    db_host: str
    db_port: int = 3306
    db_name: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    debug: bool = False
    environment: str = "development"

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
settings = Settings()