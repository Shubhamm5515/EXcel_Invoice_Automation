"""
pCloud Storage Integration - 10GB FREE, No Network Issues
Reliable cloud storage with excellent API support
"""
import requests
import os
from datetime import datetime
from typing import Optional
import zipfile
import io


class PCloudStorage:
    """Handle pCloud uploads with month-wise organization"""
    
    def __init__(self, access_token: str = None):
        """
        Initialize pCloud client
        
        Args:
            access_token: pCloud access token (from environment or parameter)
        """
        # Import settings here to avoid circular import
        from config import setting