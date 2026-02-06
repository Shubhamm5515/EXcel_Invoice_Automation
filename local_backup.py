"""
Local Backup with Month-wise Organization
No internet required - works offline
"""
import os
import shutil
from datetime import datetime
from typing import Optional
import zipfile


class LocalBackup:
    """Organize invoices locally in month-wise folders"""
    
    def __init__(self, backup_root: str = "invoice_backup"):
        """
        Initialize local backup
 