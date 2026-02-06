"""
Configuration management for Hill Drive Invoice API
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # OCR.space Configuration
    ocr_space_api_key: str
    ocr_space_api_url: str = "https://api.ocr.space/parse/image"
    
    # Gemini AI Configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    use_gemini: bool = False  # Enable/disable Gemini processing
    
    # OpenRouter AI Configuration
    openrouter_api_key: str = ""
    openrouter_model: str = "google/gemini-2.0-flash-exp:free"
    use_openrouter: bool = True  # Enable/disable OpenRouter processing
    
    # File Upload Configuration
    max_file_size_mb: int = 5
    allowed_extensions: str = "jpg,jpeg,png,pdf"  # Store as comma-separated string
    
    # Template Configuration
    template_path: str = "inn sample.xlsx"
    output_dir: str = "generated_invoices"
    use_master_file: bool = True  # If True, all invoices go to one file as sheets
    master_file_path: str = "generated_invoices/all_invoices.xlsx"
    
    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://localhost:8080"
    
    # Telegram Bot Configuration (RECOMMENDED - Works everywhere!)
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Convert comma-separated extensions to list"""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def max_file_size_bytes(self) -> int:
        """Convert MB to bytes"""
        return self.max_file_size_mb * 1024 * 1024


# Create settings instance
settings = Settings()

# Ensure output directory exists
os.makedirs(settings.output_dir, exist_ok=True)
