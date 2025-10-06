"""
Configuration management for the Mind Map AI API.
Handles environment variables and application settings.
"""

import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings and configuration."""
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./mindmap.db")
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # Hugging Face Configuration
    HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN")
    HF_API_BASE_URL: str = os.getenv("HF_API_BASE_URL", "https://api-inference.huggingface.co")
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")
    CORS_CREDENTIALS: bool = os.getenv("CORS_CREDENTIALS", "true").lower() == "true"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # File Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    
    # AI Pipeline Configuration
    AI_PIPELINE_ENABLED: bool = os.getenv("AI_PIPELINE_ENABLED", "true").lower() == "true"
    AI_FALLBACK_MODE: bool = os.getenv("AI_FALLBACK_MODE", "true").lower() == "true"
    AI_RATE_LIMIT: int = int(os.getenv("AI_RATE_LIMIT", "100"))
    
    # Export Configuration
    EXPORT_FORMATS: List[str] = os.getenv("EXPORT_FORMATS", "json,csv,xml").split(",")
    MAX_EXPORT_NODES: int = int(os.getenv("MAX_EXPORT_NODES", "1000"))
    
    # Application Info
    APP_NAME: str = "Mind Map AI API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Backend API for AI-powered mind map creation and management"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings


def is_development() -> bool:
    """Check if running in development mode."""
    return settings.DEBUG


def is_production() -> bool:
    """Check if running in production mode."""
    return not settings.DEBUG
