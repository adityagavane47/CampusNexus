"""
CampusNexus - Backend Configuration
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Algorand Network
    algorand_network: str = "testnet"
    algorand_algod_address: str = "https://testnet-api.algonode.cloud"
    algorand_indexer_address: str = "https://testnet-idx.algonode.cloud"
    
    # JWT Configuration
    jwt_secret_key: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    
    # College Information
    college_name: str = "VIT Pune"
    
    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # OAuth Configuration
    google_client_id: str = ""
    google_client_secret: str = ""
    github_client_id: str = ""
    github_client_secret: str = ""
    
    # OAuth Redirect URIs
    oauth_redirect_uri: str = "http://localhost:8000/api/oauth"
    frontend_url: str = "http://localhost:5173"
    
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
