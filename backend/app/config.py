import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    algorand_network: str = "testnet"
    algorand_algod_address: str = "https://testnet-api.algonode.cloud"
    algorand_indexer_address: str = "https://testnet-idx.algonode.cloud"
    
    jwt_secret_key: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    
    college_name: str = "CampusNexus"
    
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    google_client_id: str = ""
    google_client_secret: str = ""
    github_client_id: str = ""
    github_client_secret: str = ""
    
    oauth_redirect_uri: str = "http://localhost:8000/api/oauth"
    frontend_url: str = "http://localhost:5173"
    
    pinata_api_key: str = ""
    pinata_secret: str = ""
    
    algorand_algod_token: str = ""
    
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:

    return Settings()
