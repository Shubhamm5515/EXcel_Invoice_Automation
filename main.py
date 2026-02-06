"""
Hill Drive Invoice Automation - Entry Point
Redirects to main_new.py for backward compatibility with deployment platforms
"""
from main_new import app

# Export app for uvicorn
__all__ = ['app']

# This allows both 'main:app' and 'main_new:app' to work
if __name__ == "__main__":
    import uvicorn
    from config import settings
    
    uvicorn.run(
        "main_new:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
