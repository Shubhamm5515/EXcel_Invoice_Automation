# 🔢 Invoice Counter Management Guide

Manage your sequential invoice numbering system.

---

## 🎯 Features Fixed

### 1. ✅ Name & Address Now Fill Correctly
- Fixed cell mapping (was B10, now C10)
- Address now appears in correct cell (C12)
- Phone number in correct cell (C14)

### 2. ✅ Duplicate Invoice Number Removed
- Old invoice number in D8 is now cleared automatically
- Only one invoice number appears (in C8)

### 3. ✅ Set Starting Number
- New API endpoint to set counter
- Start from any number you want
- Change financial year

---

## 📊 API Endpoints

### 1. Check Current Counter Status

```
GET /api/counter/status
```

**Response:**
```json
{
  "current_number": 41,
  "financial_year": "2025-26",
  "next_invoice": "HD/2025-26/042",
  "last_invoice": "HD/2025-26/041"
}
```

---

### 2. Set Counter to Specific Number

```
POST /api/counter/set
```

**Parameters:**
- `start_number`: Number to start from (e.g., 36)
- `financial_year`: Optional (e.g., "2025-26")

**Example:**
```bash
curl -X POST "http://localhost:8001/api/counter/set" \
  -F "start_number=36" \
  -F "financial_year=2025-26"
```

**Response:**
```json
{
  "success": true,
  "message": "Counter set successfully",
  "next_invoice": "HD/2025-26/036",
  "financial_year": "2025-26",
  "start_number": 36
}
```

**Next invoice created will be:** `HD/2025-26/036`

---

### 3. Reset Counter for New Financial Year

```
POST /api/counter/reset
```

**Parameters:**
- `financial_year`: Optional (e.g., "2026-27")

**Example:**
```bash
curl -X POST "http://localhost:8001/api/counter/reset" \
  -F "financial_year=2026-27"
```

**Response:**
```json
{
  "success": true,
  "message": "Counter reset for financial year 2026-27",
  "next_invoice": "HD/2026-27/001",
  "financial_year": "2026-27"
}
```

---

## 💻 Usage Examples

### Check Current Status

```javascript
// JavaScript
fetch('/api/counter/status')
  .then(res => res.json())
  .then(data => {
    console.log(`Next invoice: ${data.next_invoice}`);
    console.log(`Current: ${data.current_number}`);
  });
```

```python
# Python
import requests

response = requests.get('http://localhost:8001/api/counter/status')
data = response.json()
print(f"Next invoice: {data['next_invoice']}")
```

---

### Set Starting Number

```javascript
// JavaScript - Set to start from 36
const formData = new FormData();
formData.append('start_number', '36');
formData.append('financial_year', '2025-26');

fetch('/api/counter/set', {
  method: 'POST',
  body: formData
})
  .then(res => res.json())
  .then(data => console.log(data.next_invoice));
```

```python
# Python - Set to start from 36
import requests

response = requests.post(
    'http://localhost:8001/api/counter/set',
    data={
        'start_number': 36,
        'financial_year': '2025-26'
    }
)
print(response.json())
```

---

### Reset for New Year

```javascript
// JavaScript - Reset for 2026-27
const formData = new FormData();
formData.append('financial_year', '2026-27');

fetch('/api/counter/reset', {
  method: 'POST',
  body: formData
})
  .then(res => res.json())
  .then(data => console.log(`Reset! Next: ${data.next_invoice}`));
```

---

## 🎯 Common Scenarios

### Scenario 1: Start from HD/2025-26/036

```bash
curl -X POST "http://localhost:8001/api/counter/set" \
  -F "start_number=36" \
  -F "financial_year=2025-26"
```

Next invoices will be:
- HD/2025-26/036
- HD/2025-26/037
- HD/2025-26/038
- ...

---

### Scenario 2: New Financial Year (April 2026)

```bash
curl -X POST "http://localhost:8001/api/counter/reset" \
  -F "financial_year=2026-27"
```

Next invoices will be:
- HD/2026-27/001
- HD/2026-27/002
- HD/2026-27/003
- ...

---

### Scenario 3: Continue from Current

Just create invoices normally. Counter auto-increments!

---

## 🔧 Manual Counter Edit

You can also edit `invoice_counter.json` directly:

```json
{
  "last_invoice_number": 35,
  "financial_year": "2025-26"
}
```

**To start from 036:**
```json
{
  "last_invoice_number": 35,
  "financial_year": "2025-26"
}
```

Next invoice will be 036 (35 + 1).

---

## ⚠️ Important Notes

### 1. Counter is Persistent
- Stored in `invoice_counter.json`
- Survives server restarts
- Backup this file!

### 2. Financial Year Auto-Detection
- If not specified, uses current year
- Format: YYYY-YY (e.g., 2025-26)
- April to March cycle

### 3. No Duplicates
- Counter always increments
- Can't go backwards
- Each invoice gets unique number

### 4. Backup Counter File
```bash
# Backup
cp invoice_counter.json invoice_counter.backup.json

# Restore
cp invoice_counter.backup.json invoice_counter.json
```

---

## 📱 Web Interface Integration

Add to your frontend:

```html
<div class="counter-status">
  <h3>Invoice Counter</h3>
  <p>Next Invoice: <span id="next-invoice">Loading...</span></p>
  <button onclick="showSetCounter()">Set Counter</button>
</div>

<script>
// Load counter status
async function loadCounterStatus() {
  const response = await fetch('/api/counter/status');
  const data = await response.json();
  document.getElementById('next-invoice').textContent = data.next_invoice;
}

// Set counter
async function setCounter(startNumber, financialYear) {
  const formData = new FormData();
  formData.append('start_number', startNumber);
  formData.append('financial_year', financialYear);
  
  const response = await fetch('/api/counter/set', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  alert(`Counter set! Next invoice: ${data.next_invoice}`);
  loadCounterStatus();
}

// Load on page load
loadCounterStatus();
</script>
```

---

## ✅ Testing

### Test 1: Check Status
```bash
curl http://localhost:8001/api/counter/status
```

### Test 2: Set to 036
```bash
curl -X POST "http://localhost:8001/api/counter/set" \
  -F "start_number=36" \
  -F "financial_year=2025-26"
```

### Test 3: Create Invoice
Create an invoice and verify it's HD/2025-26/036

### Test 4: Create Another
Next invoice should be HD/2025-26/037

---

## 🎉 Summary

Your invoice counter now:
- ✅ Starts from any number you choose
- ✅ Auto-increments sequentially
- ✅ Handles financial year changes
- ✅ No duplicate numbers
- ✅ Persistent across restarts
- ✅ Easy to manage via API

---

## 🆘 Troubleshooting

### Issue: Counter not incrementing

**Fix:** Check `invoice_counter.json` exists and is valid JSON

### Issue: Wrong financial year

**Fix:** Use `/api/counter/set` to set correct year

### Issue: Want to skip numbers

**Fix:** Set counter to desired number minus 1

Example: To get HD/2025-26/050 next:
```bash
curl -X POST "http://localhost:8001/api/counter/set" \
  -F "start_number=50"
```

---

**Your invoice numbering is now fully manageable! 🔢✨**
