// Hill Drive Invoice Generator - JavaScript

const API_BASE_URL = window.location.origin;
let selectedFiles = []; // Changed to array for multiple files

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeUpload();
    checkAPIStatus();
    loadInvoices();
});

// Tab Management
function initializeTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked
            btn.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
            
            // Load invoices when switching to invoices tab
            if (tabName === 'invoices') {
                loadInvoices();
            }
        });
    });
}

// File Upload Management - Multiple Files
function initializeUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // File selected
    fileInput.addEventListener('change', (e) => {
        handleFileSelect(Array.from(e.target.files));
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFileSelect(Array.from(e.dataTransfer.files));
    });
}

function handleFileSelect(files) {
    if (!files || files.length === 0) return;
    
    // Validate files
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];
    const maxSize = 5 * 1024 * 1024; // 5MB per file
    
    for (const file of files) {
        if (!validTypes.includes(file.type)) {
            showError(`Invalid file type: ${file.name}. Please upload JPG, PNG, or PDF files.`);
            continue;
        }
        
        if (file.size > maxSize) {
            showError(`File too large: ${file.name}. Maximum size is 5MB.`);
            continue;
        }
        
        selectedFiles.push(file);
    }
    
    if (selectedFiles.length > 0) {
        displayFilePreviews();
        document.getElementById('generateBtn').disabled = false;
    }
}

function displayFilePreviews() {
    const previewContainer = document.getElementById('previewContainer');
    const previewGrid = document.getElementById('previewGrid');
    const fileCount = document.getElementById('fileCount');
    
    previewContainer.style.display = 'block';
    document.getElementById('uploadArea').style.display = 'none';
    fileCount.textContent = selectedFiles.length;
    
    previewGrid.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const previewItem = document.createElement('div');
            previewItem.style.cssText = 'position: relative; border: 2px solid var(--border-color); border-radius: 8px; overflow: hidden;';
            
            if (file.type === 'application/pdf') {
                previewItem.innerHTML = `
                    <div style="padding: 20px; text-align: center; background: #f1f5f9;">
                        <div style="font-size: 48px;">📄</div>
                        <div style="font-size: 12px; margin-top: 8px;">${file.name}</div>
                    </div>
                    <button class="btn-close" onclick="removeFile(${index})" style="position: absolute; top: 5px; right: 5px;">✕</button>
                `;
            } else {
                previewItem.innerHTML = `
                    <img src="${e.target.result}" style="width: 100%; height: 150px; object-fit: cover;">
                    <button class="btn-close" onclick="removeFile(${index})" style="position: absolute; top: 5px; right: 5px;">✕</button>
                `;
            }
            
            previewGrid.appendChild(previewItem);
        };
        reader.readAsDataURL(file);
    });
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    
    if (selectedFiles.length === 0) {
        clearAllUploads();
    } else {
        displayFilePreviews();
    }
}

function clearAllUploads() {
    selectedFiles = [];
    document.getElementById('fileInput').value = '';
    document.getElementById('uploadArea').style.display = 'block';
    document.getElementById('previewContainer').style.display = 'none';
    document.getElementById('generateBtn').disabled = true;
}

function clearForm() {
    clearAllUploads();
    document.getElementById('userText').value = '';
    document.getElementById('resultContainer').style.display = 'none';
}

// Generate Invoice from OCR - Multiple Files
async function generateInvoice() {
    if (selectedFiles.length === 0) {
        showError('Please select at least one file');
        return;
    }
    
    const generateBtn = document.getElementById('generateBtn');
    const btnText = generateBtn.querySelector('.btn-text');
    const btnLoader = generateBtn.querySelector('.btn-loader');
    const progressContainer = document.getElementById('progressContainer');
    const resultContainer = document.getElementById('resultContainer');
    
    // Show loading state
    generateBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    progressContainer.style.display = 'block';
    resultContainer.style.display = 'none';
    
    try {
        let combinedOcrText = '';
        
        // Process multiple files
        if (selectedFiles.length > 1) {
            document.getElementById('progressText').textContent = `Processing ${selectedFiles.length} files...`;
            
            // Extract text from all files
            for (let i = 0; i < selectedFiles.length; i++) {
                document.getElementById('progressText').textContent = `Processing file ${i + 1} of ${selectedFiles.length}...`;
                
                const formData = new FormData();
                formData.append('file', selectedFiles[i]);
                formData.append('language', 'eng');
                
                const ocrResponse = await fetch(`${API_BASE_URL}/api/ocr/extract`, {
                    method: 'POST',
                    body: formData
                });
                
                const ocrResult = await ocrResponse.json();
                
                if (ocrResult.success && ocrResult.text) {
                    combinedOcrText += `\n--- From ${selectedFiles[i].name} ---\n${ocrResult.text}\n`;
                }
            }
        } else {
            // Single file
            document.getElementById('progressText').textContent = 'Extracting text from image...';
            
            const formData = new FormData();
            formData.append('file', selectedFiles[0]);
            formData.append('language', 'eng');
            
            const ocrResponse = await fetch(`${API_BASE_URL}/api/ocr/extract`, {
                method: 'POST',
                body: formData
            });
            
            const ocrResult = await ocrResponse.json();
            
            if (ocrResult.success && ocrResult.text) {
                combinedOcrText = ocrResult.text;
            }
        }
        
        // Combine OCR text with user text
        const userText = document.getElementById('userText').value;
        const combinedText = `${combinedOcrText}\n\n--- Additional Information ---\n${userText}`;
        
        // Update progress
        document.getElementById('progressText').textContent = 'Generating invoice...';
        
        // Create invoice with combined information
        const invoiceFormData = new FormData();
        invoiceFormData.append('file', selectedFiles[0]); // Use first file for reference
        invoiceFormData.append('user_text', combinedText);
        invoiceFormData.append('language', 'eng');
        
        // Add document images if any
        if (selectedDocuments && selectedDocuments.length > 0) {
            for (const doc of selectedDocuments) {
                invoiceFormData.append('document_images', doc);
            }
            document.getElementById('progressText').textContent = `Generating invoice with ${selectedDocuments.length} document(s)...`;
        }
        
        const response = await fetch(`${API_BASE_URL}/api/invoice/create-from-ocr`, {
            method: 'POST',
            body: invoiceFormData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccess(result);
        } else {
            showError(result.error || 'Failed to generate invoice');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        // Reset button state
        generateBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        progressContainer.style.display = 'none';
    }
}

// Create Manual Invoice
async function createManualInvoice(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    const resultContainer = document.getElementById('manualResultContainer');
    
    // Show loading
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    resultContainer.style.display = 'none';
    
    try {
        // Prepare data
        const data = {
            customer_name: document.getElementById('customerName').value,
            mobile_number: document.getElementById('mobileNumber').value,
            vehicle_name: document.getElementById('vehicleName').value,
            vehicle_number: document.getElementById('vehicleNumber').value || null,
            start_datetime: formatDateTime(document.getElementById('startDate').value),
            end_datetime: formatDateTime(document.getElementById('endDate').value),
            duration_days: parseInt(document.getElementById('durationDays').value),
            base_rent: parseFloat(document.getElementById('baseRent').value),
            included_km: parseInt(document.getElementById('includedKm').value) || null,
            extra_km: parseInt(document.getElementById('extraKm').value) || null,
            extra_km_rate: parseFloat(document.getElementById('extraKmRate').value) || null,
            total_amount: parseFloat(document.getElementById('totalAmount').value),
            advance_paid: parseFloat(document.getElementById('advancePaid').value) || null,
            payment_mode: document.getElementById('paymentMode').value,
            address: document.getElementById('address').value || null
        };
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/api/invoice/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccess(result, 'manualResultContainer');
            form.reset();
        } else {
            showError(result.error || 'Failed to create invoice', 'manualResultContainer');
        }
    } catch (error) {
        showError('Network error: ' + error.message, 'manualResultContainer');
    } finally {
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Load Invoices List
async function loadInvoices() {
    const invoicesList = document.getElementById('invoicesList');
    invoicesList.innerHTML = '<div class="loading">Loading invoices...</div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/invoice/list?limit=50`);
        const result = await response.json();
        
        if (result.invoices && result.invoices.length > 0) {
            invoicesList.innerHTML = result.invoices.map(invoice => `
                <div class="invoice-item">
                    <div class="invoice-info">
                        <h3>${invoice.invoice_id}</h3>
                        <div class="invoice-meta">
                            Created: ${formatDate(invoice.created_at)} | 
                            Size: ${formatFileSize(invoice.size_bytes)}
                        </div>
                    </div>
                    <div class="invoice-actions">
                        <button class="btn-icon" onclick="downloadInvoice('${invoice.invoice_id}')" title="Download">
                            📥
                        </button>
                        <button class="btn-icon delete" onclick="deleteInvoice('${invoice.invoice_id}')" title="Delete">
                            🗑️
                        </button>
                    </div>
                </div>
            `).join('');
        } else {
            invoicesList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📋</div>
                    <p>No invoices generated yet</p>
                    <p style="font-size: 14px; margin-top: 8px;">Upload a booking slip or enter details manually to create your first invoice</p>
                </div>
            `;
        }
    } catch (error) {
        invoicesList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">⚠️</div>
                <p>Failed to load invoices</p>
                <button class="btn btn-secondary btn-sm" onclick="loadInvoices()">Retry</button>
            </div>
        `;
    }
}

// Download Invoice
async function downloadInvoice(invoiceId) {
    try {
        window.location.href = `${API_BASE_URL}/api/invoice/download/${invoiceId}`;
    } catch (error) {
        showError('Failed to download invoice');
    }
}

// Delete Invoice
async function deleteInvoice(invoiceId) {
    if (!confirm('Are you sure you want to delete this invoice?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/invoice/delete/${invoiceId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            loadInvoices();
        } else {
            showError('Failed to delete invoice');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

// Check API Status
async function checkAPIStatus() {
    const statusElement = document.getElementById('apiStatus');
    
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const result = await response.json();
        
        if (result.status === 'healthy') {
            statusElement.classList.add('online');
            statusElement.querySelector('span:last-child').textContent = 'API Online';
        } else {
            statusElement.classList.add('offline');
            statusElement.querySelector('span:last-child').textContent = 'API Offline';
        }
    } catch (error) {
        statusElement.classList.add('offline');
        statusElement.querySelector('span:last-child').textContent = 'API Offline';
    }
}

// Show Success Message
function showSuccess(result, containerId = 'resultContainer') {
    const container = document.getElementById(containerId);
    container.className = 'result-container result-success';
    container.innerHTML = `
        <div class="result-title">✅ Invoice Generated Successfully!</div>
        <div class="result-details">
            <div class="result-item">
                <span class="result-label">Invoice ID:</span>
                <span class="result-value">${result.invoice_id}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Confidence:</span>
                <span class="result-value">${result.confidence || 'N/A'}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Calculation Verified:</span>
                <span class="result-value">${result.calculation_verified ? '✓ Yes' : '✗ No'}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Processing Time:</span>
                <span class="result-value">${result.processing_time_ms}ms</span>
            </div>
        </div>
        <div class="result-actions">
            <button class="btn btn-primary" onclick="downloadInvoice('${result.invoice_id}')">
                📥 Download Invoice
            </button>
            <button class="btn btn-secondary" onclick="loadInvoices(); document.querySelector('[data-tab=invoices]').click()">
                📋 View All Invoices
            </button>
        </div>
    `;
    container.style.display = 'block';
}

// Show Error Message
function showError(message, containerId = 'resultContainer') {
    const container = document.getElementById(containerId);
    container.className = 'result-container result-error';
    container.innerHTML = `
        <div class="result-title">❌ Error</div>
        <p>${message}</p>
    `;
    container.style.display = 'block';
}

// Utility Functions
function formatDateTime(dateTimeStr) {
    if (!dateTimeStr) return null;
    const date = new Date(dateTimeStr);
    return date.toISOString().slice(0, 16).replace('T', ' ');
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleString();
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Document Upload Management
let selectedDocuments = [];

function initializeDocumentUpload() {
    const documentUploadArea = document.getElementById('documentUploadArea');
    const documentInput = document.getElementById('documentInput');
    
    if (!documentUploadArea || !documentInput) return;
    
    // Click to upload
    documentUploadArea.addEventListener('click', (e) => {
        if (e.target.tagName !== 'BUTTON') {
            documentInput.click();
        }
    });
    
    // File selected
    documentInput.addEventListener('change', (e) => {
        handleDocumentSelect(Array.from(e.target.files));
    });
    
    // Drag and drop
    documentUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        documentUploadArea.classList.add('dragover');
    });
    
    documentUploadArea.addEventListener('dragleave', () => {
        documentUploadArea.classList.remove('dragover');
    });
    
    documentUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        documentUploadArea.classList.remove('dragover');
        handleDocumentSelect(Array.from(e.dataTransfer.files));
    });
}

function handleDocumentSelect(files) {
    if (!files || files.length === 0) return;
    
    // Validate files
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    const maxSize = 5 * 1024 * 1024; // 5MB per file
    
    for (const file of files) {
        if (!validTypes.includes(file.type)) {
            showError(`Invalid document type: ${file.name}. Please upload JPG or PNG images.`);
            continue;
        }
        
        if (file.size > maxSize) {
            showError(`Document too large: ${file.name}. Maximum size is 5MB.`);
            continue;
        }
        
        selectedDocuments.push(file);
    }
    
    if (selectedDocuments.length > 0) {
        displayDocumentPreviews();
    }
}

function displayDocumentPreviews() {
    const previewContainer = document.getElementById('documentPreviewContainer');
    const previewGrid = document.getElementById('documentPreviewGrid');
    const documentCount = document.getElementById('documentCount');
    
    if (!previewContainer || !previewGrid) return;
    
    previewContainer.style.display = 'block';
    documentCount.textContent = selectedDocuments.length;
    previewGrid.innerHTML = '';
    
    selectedDocuments.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            previewItem.innerHTML = `
                <img src="${e.target.result}" alt="${file.name}">
                <div class="preview-info">
                    <span class="preview-name">${file.name}</span>
                    <button class="preview-remove" onclick="removeDocument(${index})">×</button>
                </div>
            `;
            previewGrid.appendChild(previewItem);
        };
        reader.readAsDataURL(file);
    });
}

function removeDocument(index) {
    selectedDocuments.splice(index, 1);
    if (selectedDocuments.length > 0) {
        displayDocumentPreviews();
    } else {
        document.getElementById('documentPreviewContainer').style.display = 'none';
    }
}

function clearDocuments() {
    selectedDocuments = [];
    document.getElementById('documentPreviewContainer').style.display = 'none';
    document.getElementById('documentInput').value = '';
}

// Initialize document upload when page loads
document.addEventListener('DOMContentLoaded', () => {
    initializeDocumentUpload();
});
