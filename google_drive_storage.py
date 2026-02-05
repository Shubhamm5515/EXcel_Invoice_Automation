"""
Google Drive Storage Integration
Automatically uploads invoices to Google Drive in month-wise folders
"""
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
import os
from typing import Optional

class GoogleDriveStorage:
    """Handle Google Drive uploads with month-wise organization"""
    
    def __init__(self, credentials_file: str = 'google_credentials.json'):
        """
        Initialize Google Drive client
        
        Args:
            credentials_file: Path to service account JSON file
        """
        self.credentials_file = credentials_file
        self.service = None
        self.root_folder_id = None
        
        if os.path.exists(credentials_file):
            self._initialize_service()
        else:
            print(f"⚠️  Google Drive credentials not found: {credentials_file}")
            print(f"   Upload feature disabled. See GOOGLE_DRIVE_SETUP.md")
    
    def _initialize_service(self):
        """Initialize Google Drive API service"""
        try:
            SCOPES = ['https://www.googleapis.com/auth/drive.file']
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file, scopes=SCOPES
            )
            self.service = build('drive', 'v3', credentials=credentials)
            print("✅ Google Drive connected")
        except Exception as e:
            print(f"⚠️  Google Drive initialization failed: {e}")
            self.service = None
    
    def _get_or_create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """Get existing folder or create new one"""
        if not self.service:
            return None
        
        try:
            # Search for existing folder
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            if parent_id:
                query += f" and '{parent_id}' in parents"
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                return folders[0]['id']
            
            # Create new folder
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            return folder.get('id')
        
        except Exception as e:
            print(f"⚠️  Folder creation failed: {e}")
            return None
    
    def upload_invoice(self, file_path: str, invoice_date: Optional[datetime] = None) -> Optional[str]:
        """
        Upload invoice to Google Drive in month-wise folder
        
        Args:
            file_path: Local path to invoice file
            invoice_date: Date of invoice (defaults to today)
        
        Returns:
            Google Drive file ID or None
        """
        if not self.service:
            return None
        
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {file_path}")
            return None
        
        try:
            # Use provided date or current date
            date = invoice_date or datetime.now()
            
            # Create folder structure: Hill Drive Invoices/2026/Feb 2026/
            root_folder = self._get_or_create_folder('Hill Drive Invoices')
            year_folder = self._get_or_create_folder(str(date.year), root_folder)
            month_folder = self._get_or_create_folder(
                date.strftime('%b %Y'),  # e.g., "Feb 2026"
                year_folder
            )
            
            if not month_folder:
                print("⚠️  Could not create month folder")
                return None
            
            # Upload file
            file_name = os.path.basename(file_path)
            file_metadata = {
                'name': file_name,
                'parents': [month_folder]
            }
            
            media = MediaFileUpload(
                file_path,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            file_id = file.get('id')
            web_link = file.get('webViewLink')
            
            print(f"✅ Uploaded to Google Drive: {file_name}")
            print(f"   Folder: {date.strftime('%b %Y')}")
            print(f"   Link: {web_link}")
            
            return file_id
        
        except Exception as e:
            print(f"⚠️  Upload failed: {e}")
            return None
    
    def download_month_folder(self, year: int, month: int, output_dir: str = 'downloads'):
        """
        Download all invoices from a specific month
        
        Args:
            year: Year (e.g., 2026)
            month: Month (1-12)
            output_dir: Local directory to save files
        """
        if not self.service:
            print("⚠️  Google Drive not connected")
            return
        
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Get month folder
            date = datetime(year, month, 1)
            month_name = date.strftime('%b %Y')
            
            # Find folder
            root_folder = self._get_or_create_folder('Hill Drive Invoices')
            year_folder = self._get_or_create_folder(str(year), root_folder)
            month_folder = self._get_or_create_folder(month_name, year_folder)
            
            if not month_folder:
                print(f"⚠️  Folder not found: {month_name}")
                return
            
            # List files in folder
            query = f"'{month_folder}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                fields='files(id, name)'
            ).execute()
            
            files = results.get('files', [])
            
            if not files:
                print(f"📁 No files in {month_name}")
                return
            
            print(f"\n📥 Downloading {len(files)} files from {month_name}...")
            
            # Download each file
            from googleapiclient.http import MediaIoBaseDownload
            import io
            
            for file in files:
                file_id = file['id']
                file_name = file['name']
                
                request = self.service.files().get_media(fileId=file_id)
                file_path = os.path.join(output_dir, file_name)
                
                fh = io.FileIO(file_path, 'wb')
                downloader = MediaIoBaseDownload(fh, request)
                
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                
                print(f"   ✅ {file_name}")
            
            print(f"\n✅ Downloaded {len(files)} files to: {output_dir}")
        
        except Exception as e:
            print(f"⚠️  Download failed: {e}")
    
    def get_month_summary(self, year: int, month: int) -> dict:
        """Get summary of invoices in a month"""
        if not self.service:
            return {'error': 'Google Drive not connected'}
        
        try:
            date = datetime(year, month, 1)
            month_name = date.strftime('%b %Y')
            
            # Find folder
            root_folder = self._get_or_create_folder('Hill Drive Invoices')
            year_folder = self._get_or_create_folder(str(year), root_folder)
            month_folder = self._get_or_create_folder(month_name, year_folder)
            
            if not month_folder:
                return {'month': month_name, 'count': 0, 'files': []}
            
            # List files
            query = f"'{month_folder}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                fields='files(id, name, createdTime, size, webViewLink)'
            ).execute()
            
            files = results.get('files', [])
            
            return {
                'month': month_name,
                'count': len(files),
                'files': files
            }
        
        except Exception as e:
            return {'error': str(e)}


# Example usage
if __name__ == '__main__':
    storage = GoogleDriveStorage()
    
    # Test upload
    # storage.upload_invoice('generated_invoices/test.xlsx')
    
    # Test download month
    # storage.download_month_folder(2026, 2, 'downloads/Feb_2026')
    
    # Get month summary
    # summary = storage.get_month_summary(2026, 2)
    # print(summary)
