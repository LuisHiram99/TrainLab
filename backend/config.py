from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import SecretStr, EmailStr, Field, computed_field
from typing import Annotated, Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "TrainLab"
    port: Annotated[int, Field(gt=0, lt=65536)] = 8000
    ENVIRONMENT: str
    
    # Option 1: Complete DATABASE_URL (if provided, this takes precedence)
    database_url: Optional[SecretStr] = None
    
    # Option 2: Individual database connection parameters (optional if DATABASE_URL is provided)
    db_user: Optional[str] = None
    db_password: Optional[SecretStr] = None
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: Optional[str] = None
    
    upload_dir: Path = Path("uploads")
    
    @computed_field
    @property
    def DATABASE_URL(self) -> SecretStr:
        """Get DATABASE_URL, either from direct setting or constructed from individual parameters"""
        if self.database_url:
            return self.database_url
        
        # Construct from individual parameters (default to async for the app)
        if not all([self.db_user, self.db_password, self.db_name]):
            raise ValueError("Either 'database_url' or all of 'db_user', 'db_password', 'db_name' must be provided")
        
        url = f"postgresql+asyncpg://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}"
        return SecretStr(url)
    
    def get_sync_database_url(self) -> str:
        """Get synchronous DATABASE_URL for tools like Alembic that don't support async"""
        url = self.DATABASE_URL.get_secret_value()
        # Convert async driver to sync driver for Alembic
        if "+asyncpg://" in url:
            url = url.replace("+asyncpg://", "+psycopg2://")
        elif "postgresql://" in url and "+psycopg2://" not in url:
            # If it's a plain postgresql:// URL, make it explicit psycopg2
            url = url.replace("postgresql://", "postgresql+psycopg2://")
        return url