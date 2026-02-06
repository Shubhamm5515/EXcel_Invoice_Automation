"""
Telegram Bot Storage - FREE Unlimited Storage
Most reliable option - works everywhere, no blocking
"""
import requests
import os
from datetime import datetime
from typing import Optional


class TelegramStorage:
    """Upload invoices to Telegram channel/chat"""
    
    def __init__(self, bot_token: str = None, chat_id: str = None):
        """
        Initialize Telegram bot
        
        Args:
            bot_token: Telegram bot token (from @BotFather)
            chat_id: Your Telegram chat ID or channel ID
        """
        # Import settings here to avoid circular import
        from config import settings
        
        self.bot_token = bot_token or settings.telegram_bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or settings.telegram_chat_id or os.getenv('TELEGRAM_CHAT_ID')
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}" if self.bot_token else None
        
        if self.bot_token and self.chat_id:
            try:
                # Test connection
                response = requests.get(f"{self.api_url}/getMe", timeout=5)
                if response.status_code == 200:
                    bot_info = response.json()
                    print("✅ Telegram Bot connected")
                    print(f"   Bot: @{bot_info['result']['username']}")
                    print(f"   Storage: UNLIMITED FREE")
                else:
                    print(f"⚠️  Telegram bot token invalid")
                    self.bot_token = None
            except Exception as e:
                print(f"⚠️  Telegram connection failed: {e}")
                self.bot_token = None
        else:
            print(f"⚠️  Telegram credentials not found")
            print(f"   Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env file")
    
    def upload_invoice(self, file_path: str, invoice_date: Optional[datetime] = None) -> Optional[str]:
        """
        Upload invoice to Telegram
        
        Args:
            file_path: Local path to invoice file
            invoice_date: Date of invoice (defaults to today)
        
        Returns:
            Telegram file_id or None
        """
        if not self.bot_token or not self.chat_id:
            return None
        
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {file_path}")
            return None
        
        try:
            # Use provided date or current date
            date = invoice_date or datetime.now()
            month_name = date.strftime('%b %Y')  # e.g., "Feb 2026"
            file_name = os.path.basename(file_path)
            
            # Create caption with folder info
            caption = f"📁 Hill Drive Invoice\n📅 {month_name}\n📄 {file_name}"
            
            print(f"📤 Uploading to Telegram: {file_name}")
            
            # Upload file to Telegram
            with open(file_path, 'rb') as file:
                files = {'document': file}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption
                }
                
                response = requests.post(
                    f"{self.api_url}/sendDocument",
                    files=files,
                    data=data,
                    timeout=60
                )
            
            if response.status_code == 200:
                result = response.json()
                file_id = result['result']['document']['file_id']
                
                print(f"✅ Uploaded to Telegram: {file_name}")
                print(f"   Folder: {month_name}")
                print(f"   File ID: {file_id[:20]}...")
                
                return file_id
            else:
                print(f"⚠️  Telegram upload failed: {response.text}")
                return None
        
        except Exception as e:
            print(f"⚠️  Telegram upload failed: {e}")
            return None
    
    def get_file_link(self, file_id: str) -> Optional[str]:
        """Get download link for a file"""
        if not self.bot_token:
            return None
        
        try:
            response = requests.get(
                f"{self.api_url}/getFile",
                params={'file_id': file_id},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                file_path = result['result']['file_path']
                return f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"
            
            return None
        except Exception as e:
            print(f"⚠️  Failed to get file link: {e}")
            return None


# Example usage
if __name__ == '__main__':
    storage = TelegramStorage()
    
    # Test upload
    # storage.upload_invoice('generated_invoices/test.xlsx')
