"""
MEGA Cloud Storage Integration - FREE 20GB Storage
Automatically uploads invoices to MEGA in month-wise folders
"""
from mega import Mega
from datetime import datetime
import os
from typing import Optional
import zipfile
import io


class MegaStorage:
    """Handle MEGA uploads with month-wise organization"""
    
    def __init__(self, email: str = None, password: str = None):
        """
        Initialize MEGA client
        
        Args:
            email: MEGA account email (from environment or parameter)
            password: MEGA account password (from environment or parameter)
        """
        # Import settings here to avoid circular import
        from config import settings
        
        self.email = email or settings.mega_email or os.getenv('MEGA_EMAIL')
        self.password = password or settings.mega_password or os.getenv('MEGA_PASSWORD')
        self.mega = None
        
        if self.email and self.password:
            try:
                self.mega = Mega()
                self.m = self.mega.login(self.email, self.password)
                print("✅ MEGA connected")
                print(f"   Account: {self.email}")
                print(f"   Storage: 20 GB FREE")
            except Exception as e:
                print(f"⚠️  MEGA login failed: {e}")
                print(f"   Check your email and password in .env file")
                self.mega = None
                self.m = None
        else:
            print(f"⚠️  MEGA credentials not found")
            print(f"   Set MEGA_EMAIL and MEGA_PASSWORD in .env file")
            self.m = None
    
    def upload_invoice(self, file_path: str, invoice_date: Optional[datetime] = None) -> Optional[str]:
        """
        Upload invoice to MEGA in month-wise folder
        
        Args:
            file_path: Local path to invoice file
            invoice_date: Date of invoice (defaults to today)
        
        Returns:
            MEGA file link or None
        """
        print(f"🔄 MEGA upload called for: {file_path}")
        
        if not self.m:
            print(f"⚠️  MEGA not connected - skipping upload")
            return None
        
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {file_path}")
            return None
        
        try:
            print(f"📤 Starting MEGA upload...")
            
            # Use provided date or current date
            date = invoice_date or datetime.now()
            
            # Create folder path: Hill Drive Invoices/2026/Feb 2026/
            year = date.year
            month_name = date.strftime('%b %Y')  # e.g., "Feb 2026"
            
            print(f"📁 Creating folder structure: /Hill Drive Invoices/{year}/{month_name}/")
            
            # Get or create folder structure
            root_folder = self._get_or_create_folder('Hill Drive Invoices')
            year_folder = self._get_or_create_folder(str(year), root_folder)
            month_folder = self._get_or_create_folder(month_name, year_folder)
            
            # Upload file
            file_name = os.path.basename(file_path)
            
            print(f"⬆️  Uploading {file_name} to MEGA...")
            
            # Upload to MEGA
            file = self.m.upload(file_path, month_folder)
            
            # Get shareable link
            link = self.m.get_upload_link(file)
            
            print(f"✅ Uploaded to MEGA: {file_name}")
            print(f"   Folder: {month_name}")
            print(f"   Link: {link}")
            
            return link
        
        except Exception as e:
            print(f"⚠️  MEGA upload failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _get_or_create_folder(self, folder_name: str, parent_folder=None):
        """Get existing folder or create new one"""
        try:
            # Get all files/folders
            files = self.m.get_files()
            
            # Search for folder
            for file_id, file_data in files.items():
                if file_data['a'] and file_data['a'].get('n') == folder_name:
                    # Check if it's in the right parent
                    if parent_folder is None:
                        # Root level folder
                        if file_data.get('p') == self.m.root_id:
                            return file_id
                    else:
                        # Child folder
                        if file_data.get('p') == parent_folder:
                            return file_id
            
            # Folder doesn't exist, create it
            if parent_folder:
                folder = self.m.create_folder(folder_name, parent_folder)
            else:
                folder = self.m.create_folder(folder_name)
            
            return folder
        
        except Exception as e:
            print(f"⚠️  Folder creation failed: {e}")
            return None
    
    def download_month_folder(self, year: int, month: int, output_dir: str = 'downloads'):
        """
        Download all invoices from a specific month
        
        Args:
            year: Year (e.g., 2026)
            month: Month (1-12)
            output_dir: Local directory to save files
        """
        if not self.m:
            print("⚠️  MEGA not connected")
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
            
            # Get all files in folder
            files = self.m.get_files()
            month_files = []
            
            for file_id, file_data in files.items():
                if file_data.get('p') == month_folder and file_data.get('t') == 0:  # t=0 means file
                    month_files.append((file_id, file_data['a']['n']))
            
            if not month_files:
                print(f"📁 No files in {month_name}")
                return
            
            print(f"\n📥 Downloading {len(month_files)} files from {month_name}...")
            
            # Download each file
            for file_id, file_name in month_files:
                file_path = os.path.join(output_dir, file_name)
                self.m.download((file_id, file_name), output_dir)
                print(f"   ✅ {file_name}")
            
            print(f"\n✅ Downloaded {len(month_files)} files to: {output_dir}")
        
        except Exception as e:
            print(f"⚠️  Download failed: {e}")
    
    def get_month_summary(self, year: int, month: int) -> dict:
        """Get summary of invoices in a month"""
        if not self.m:
            return {'error': 'MEGA not connected'}
        
        try:
            date = datetime(year, month, 1)
            month_name = date.strftime('%b %Y')
            
            # Find folder
            root_folder = self._get_or_create_folder('Hill Drive Invoices')
            year_folder = self._get_or_create_folder(str(year), root_folder)
            month_folder = self._get_or_create_folder(month_name, year_folder)
            
            if not month_folder:
                return {'month': month_name, 'count': 0, 'files': []}
            
            # Get all files in folder
            files = self.m.get_files()
            month_files = []
            
            for file_id, file_data in files.items():
                if file_data.get('p') == month_folder and file_data.get('t') == 0:  # t=0 means file
                    month_files.append({
                        'name': file_data['a']['n'],
                        'size': file_data.get('s', 0),
                        'timestamp': file_data.get('ts', 0)
                    })
            
            return {
                'month': month_name,
                'count': len(month_files),
                'files': month_files
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def download_month_as_zip(self, year: int, month: int) -> Optional[bytes]:
        """
        Download all invoices from a month as a ZIP file in memory
        
        Args:
            year: Year (e.g., 2026)
            month: Month (1-12)
        
        Returns:
            ZIP file bytes or None
        """
        if not self.m:
            return None
        
        try:
            date = datetime(year, month, 1)
            month_name = date.strftime('%b %Y')
            
            # Find folder
            root_folder = self._get_or_create_folder('Hill Drive Invoices')
            year_folder = self._get_or_create_folder(str(year), root_folder)
            month_folder = self._get_or_create_folder(month_name, year_folder)
            
            if not month_folder:
                return None
            
            # Get all files in folder
            files = self.m.get_files()
            month_files = []
            
            for file_id, file_data in files.items():
                if file_data.get('p') == month_folder and file_data.get('t') == 0:
                    month_files.append((file_id, file_data['a']['n']))
            
            if not month_files:
                return None
            
            # Create ZIP in memory
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file_id, file_name in month_files:
                    # Download file to memory
                    import tempfile
                    with tempfile.TemporaryDirectory() as temp_dir:
                        self.m.download((file_id, file_name), temp_dir)
                        temp_file_path = os.path.join(temp_dir, file_name)
                        
                        # Read and add to ZIP
                        with open(temp_file_path, 'rb') as f:
                            zip_file.writestr(file_name, f.read())
            
            zip_buffer.seek(0)
            return zip_buffer.getvalue()
        
        except Exception as e:
            print(f"⚠️  ZIP creation failed: {e}")
            return None


# Example usage
if __name__ == '__main__':
    storage = MegaStorage()
    
    # Test upload
    # storage.upload_invoice('generated_invoices/test.xlsx')
    
    # Test download month
    # storage.download_month_folder(2026, 2, 'downloads/Feb_2026')
    
    # Get month summary
    # summary = storage.get_month_summary(2026, 2)
    # print(summary)
