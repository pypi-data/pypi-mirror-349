from typing import Optional, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

class DatabaseSettings(BaseSettings):
    """Database configuration settings"""
    
    # Database type: sqlite or postgres
    DATABASE_TYPE: Literal["sqlite", "postgres"] = "sqlite"
    
    # SQLite settings
    DATABASE_PATH: str = "data/lyraios.db"
    
    # PostgreSQL settings (optional)
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: Optional[int] = 5432
    POSTGRES_DB: Optional[str] = "lyraios"
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    
    # Auto create database and tables
    AUTO_CREATE_DB: bool = True
    
    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_TYPE.lower() == "sqlite"
    
    @property
    def is_postgres(self) -> bool:
        return self.DATABASE_TYPE.lower() == "postgres"
    
    @property
    def absolute_db_path(self) -> str:
        """Get absolute path to database file"""
        if os.path.isabs(self.DATABASE_PATH):
            return self.DATABASE_PATH
        return str(Path.cwd() / self.DATABASE_PATH)
    
    @property
    def db_url(self) -> str:
        if self.is_sqlite:
            db_path = self.absolute_db_path
            # Ensure data directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            return f"sqlite:///{db_path}"
        elif self.is_postgres and all([
            self.POSTGRES_HOST,
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_DB
        ]):
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        else:
            raise ValueError("Invalid database configuration")

    # Use new SettingsConfigDict configuration method
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        extra="allow"  # Allow extra environment variables
    )

# Create global settings instance
db_settings = DatabaseSettings() 