# 📁 Google Drive Features - Complete Overview

Your invoice system now has full Google Drive integration!

---

## ✨ Features

### 1. Auto-Upload
Every invoice is automatically uploaded to Google Drive after creation.

### 2. Month-Wise Organization
Invoices organized in folders:
```
Hill Drive Invoices/
└── 2026/
    ├── Jan 2026/
    ├── Feb 2026/
    └── Mar 2026/
```

### 3. Bulk Download
Download entire month as ZIP file with one click.

### 4. Month Summary
View count and list of invoices for any month.

### 5. Team Sharing
Share folders with team members for easy access.

### 6. Mobile Access
Access invoices from Google Drive mobile app.

---

## 🔌 API Endpoints

### Check Google Drive Status
```
GET /api/drive/status
```

Response:
```json
{
  "enabled": true,
  "message": "Google Drive is connected"
}
```

---

### Get Month Summary
```
GET /api/drive/month-summary?year=2026&month=2
```

Response:
```json
{
  "month": "Feb 2026",
  "count": 15,
  "files": [
    {
      "id": "abc123xyz",
      "name": "HD-20260205-abc123.xlsx",
      "createdTime": "2026-02-05T10:30:00Z",
      "size": "45678",
      "webViewLink": "https://drive.google.com/file/d/abc123xyz/view"
    },
    ...
  ]
}
```

---

### Download Month as ZIP
```
GET /api/drive/download-month?year=2026&month=2
```

Downloads: `invoices_Feb_2026.zip`

Contains all invoices from February 2026.

---

## 💻 Usage Examples

### JavaScript (Frontend)

```javascript
// Get month summary
async function getMonthSummary(year, month) {
  const response = await fetch(
    `/api/drive/month-summary?year=${year}&month=${month}`
  );
  const data = await response.json();
  console.log(`${data.month}: ${data.count} invoices`);
  return data;
}

// Download month
function downloadMonth(year, month) {
  window.location.href = `/api/drive/download-month?year=${year}&month=${month}`;
}

// Usage
getMonthSummary(2026, 2);  // Get February summary
downloadMonth(2026, 2);     // Download February invoices
```

---

### Python (Backend)

```python
from google_drive_storage import GoogleDriveStorage

storage = GoogleDriveStorage()

# Upload invoice
file_id = storage.upload_invoice('generated_invoices/invoice.xlsx')

# Get month summary
summary = storage.get_month_summary(2026, 2)
print(f"{summary['month']}: {summary['count']} invoices")

# Download month to local folder
storage.download_month_folder(2026, 2, 'downloads/Feb_2026')
```

---

### cURL (API Testing)

```bash
# Check status
curl http://localhost:8001/api/drive/status

# Get month summary
curl "http://localhost:8001/api/drive/month-summary?year=2026&month=2"

# Download month
curl -O "http://localhost:8001/api/drive/download-month?year=2026&month=2"
```

---

## 🎯 Monthly Workflow

### Day-to-Day:
1. Create invoices as usual
2. Invoices auto-upload to Google Drive
3. No manual action needed!

### End of Month:
1. **Check count:**
   ```
   GET /api/drive/month-summary?year=2026&month=2
   ```

2. **Download all:**
   ```
   GET /api/drive/download-month?year=2026&month=2
   ```

3. **Backup:**
   - Save ZIP to external drive
   - Upload to accounting software
   - Archive for records

4. **Share with accountant:**
   - Share Google Drive folder
   - Or send ZIP file

---

## 📱 Access Methods

### 1. Web Interface (Your App)
- View month summary
- Download month as ZIP
- Create new invoices (auto-upload)

### 2. Google Drive Web
- Browse all invoices
- Download individual files
- Download entire folders
- Share with team

### 3. Google Drive Mobile App
- View invoices on phone
- Download to phone
- Share via WhatsApp/Email
- Access offline

### 4. API
- Programmatic access
- Integration with other systems
- Automated workflows

---

## 👥 Team Collaboration

### Share with Team:

1. **Accountant (Viewer):**
   - Can view and download
   - Cannot edit or delete
   - Perfect for accounting team

2. **Manager (Editor):**
   - Can view, download, upload
   - Can organize folders
   - Can delete if needed

3. **Team Member (Viewer):**
   - Can view invoices
   - Can download for reference
   - Cannot modify

### How to Share:

1. Go to Google Drive
2. Right-click "Hill Drive Invoices"
3. Click "Share"
4. Add emails with appropriate permissions
5. Click "Send"

---

## 📊 Storage & Limits

### Free Tier:
- **15 GB** storage
- Shared with Gmail and Photos
- ~30,000 invoices (500 KB each)
- Enough for years of invoices

### If You Need More:
- **100 GB:** $2/month
- **200 GB:** $3/month
- **2 TB:** $10/month

### Current Usage:
Check at: https://drive.google.com/settings/storage

---

## 🔐 Security Features

### 1. Service Account
- Dedicated account for uploads
- Limited permissions
- No human access needed

### 2. Encrypted Transfer
- All uploads via HTTPS
- Secure API communication
- Google's encryption at rest

### 3. Access Control
- Share only with authorized users
- Revoke access anytime
- Audit logs available

### 4. Backup
- Google's redundant storage
- 99.9% uptime SLA
- Automatic versioning

---

## 🎨 Frontend Integration

Add to your web interface:

### Month Summary Widget:

```html
<div class="month-summary">
  <h3>February 2026</h3>
  <p>Total Invoices: <span id="invoice-count">0</span></p>
  <button onclick="downloadMonth(2026, 2)">Download All</button>
</div>

<script>
async function loadMonthSummary() {
  const response = await fetch('/api/drive/month-summary?year=2026&month=2');
  const data = await response.json();
  document.getElementById('invoice-count').textContent = data.count;
}

function downloadMonth(year, month) {
  window.location.href = `/api/drive/download-month?year=${year}&month=${month}`;
}

loadMonthSummary();
</script>
```

---

## 📈 Analytics

### Track Usage:

```python
# Get summaries for all months
months_data = []
for month in range(1, 13):
    summary = storage.get_month_summary(2026, month)
    months_data.append({
        'month': summary['month'],
        'count': summary['count']
    })

# Find busiest month
busiest = max(months_data, key=lambda x: x['count'])
print(f"Busiest month: {busiest['month']} with {busiest['count']} invoices")
```

---

## 🔧 Advanced Features

### 1. Automatic Backup
Invoices backed up to Google Drive immediately after creation.

### 2. Version History
Google Drive keeps version history automatically.

### 3. Offline Access
Download invoices for offline access via Google Drive app.

### 4. Search
Search invoices by name/date in Google Drive.

### 5. Integration
Integrate with Google Sheets, Docs, etc.

---

## 🎉 Benefits

### For You:
- ✅ Automatic backup
- ✅ Never lose invoices
- ✅ Access from anywhere
- ✅ Easy organization

### For Your Team:
- ✅ Shared access
- ✅ Real-time updates
- ✅ Mobile access
- ✅ Easy collaboration

### For Your Business:
- ✅ Professional backup
- ✅ Audit trail
- ✅ Compliance ready
- ✅ Scalable storage

---

## 📚 Documentation

- **Quick Start:** `GOOGLE_DRIVE_QUICK_START.md`
- **Complete Setup:** `GOOGLE_DRIVE_COMPLETE_SETUP.md`
- **API Reference:** `/docs` (FastAPI Swagger UI)

---

## 🆘 Support

### Common Issues:

1. **"Credentials not found"**
   - Add `google_credentials.json` to project root

2. **"Permission denied"**
   - Enable Google Drive API
   - Check service account role

3. **"Folder not created"**
   - Check internet connection
   - Verify API quota

### Get Help:
- Google Drive API Docs: https://developers.google.com/drive
- Service Account Guide: https://cloud.google.com/iam/docs/service-accounts

---

## ✅ Setup Checklist

- [ ] Google Cloud project created
- [ ] Google Drive API enabled
- [ ] Service account created
- [ ] JSON key downloaded
- [ ] Credentials added to project
- [ ] Connection tested
- [ ] Test invoice uploaded
- [ ] Month summary works
- [ ] Bulk download works
- [ ] Team access shared

---

**Your invoice system is now fully integrated with Google Drive! 📁✨**
