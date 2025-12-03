"""
API Configuration
Environment-based configuration for the FastAPI application
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "HealthFlow Information Exchange API"
    API_VERSION: str = "2.0.0"
    API_PREFIX: str = "/api"
    
    # Security
    API_KEY: str = os.getenv("API_KEY", "dev-api-key-change-in-production")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://healthflow:healthflow@localhost:5432/healthflow_epx"
    )
    
    # Redis (optional)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # CORS
    CORS_ORIGINS: list = ["*"]  # Configure appropriately for production
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true"
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
