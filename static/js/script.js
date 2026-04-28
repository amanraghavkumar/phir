// PHIR - Frontend JavaScript
// Main application logic

document.addEventListener('DOMContentLoaded', function() {
    console.log('PHIR Application Loaded');
    initializeApp();
});

function initializeApp() {
    // Check health
    checkHealth();
    
    // Setup upload handlers if on upload page
    setupUploadHandlers();
}

function checkHealth() {
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            if (data.model_loaded) {
                console.log('✓ Model loaded and ready');
            } else {
                console.warn('⚠ Model not loaded');
            }
        })
        .catch(error => console.error('Health check failed:', error));
}

function setupUploadHandlers() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    
    if (!uploadZone || !fileInput) return;
    
    // Click to upload
    uploadZone.addEventListener('click', () => fileInput.click());
    
    // Drag and drop
    uploadZone.addEventListener('dragover', handleDragOver);
    uploadZone.addEventListener('dragleave', handleDragLeave);
    uploadZone.addEventListener('drop', handleDrop);
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
}

function handleDragOver(e) {
    e.preventDefault();
    document.getElementById('uploadZone').classList.add('dragover');
}

function handleDragLeave(e) {
    document.getElementById('uploadZone').classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    document.getElementById('uploadZone').classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
}

function handleFileSelect(file) {
    const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
    const maxSize = 50 * 1024 * 1024;
    
    if (!validTypes.includes(file.type)) {
        showError('Invalid file type. Please upload JPG, PNG, or GIF.');
        return;
    }
    
    if (file.size > maxSize) {
        showError('File too large. Maximum size is 50MB.');
        return;
    }
    
    displayPreview(file);
}

function displayPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('previewImage').src = e.target.result;
        document.getElementById('previewContainer').style.display = 'block';
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('fileSize').textContent = (file.size / 1024 / 1024).toFixed(2) + ' MB';
        document.getElementById('fileType').textContent = file.type;
        document.getElementById('analyzeBtn').disabled = false;
    };
    reader.readAsDataURL(file);
}

function analyzeImage() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        showError('Please select an image first');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    document.getElementById('loadingContainer').style.display = 'block';
    document.getElementById('resultsContainer').style.display = 'none';
    document.getElementById('errorContainer').style.display = 'none';
    
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loadingContainer').style.display = 'none';
        
        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'Prediction failed');
        }
    })
    .catch(error => {
        document.getElementById('loadingContainer').style.display = 'none';
        showError('Error: ' + error.message);
    });
}

function displayResults(data) {
    document.getElementById('predictedClass').textContent = data.predicted_class;
    
    const confidence = data.confidence;
    document.getElementById('confidenceBar').style.width = confidence + '%';
    document.getElementById('confidenceText').textContent = confidence.toFixed(2) + '%';
    
    const probsHtml = Object.entries(data.probabilities).map(([className, prob]) => `
        <div class="mb-3">
            <div class="d-flex justify-content-between mb-1">
                <small><strong>${className}</strong></small>
                <small>${prob.toFixed(2)}%</small>
            </div>
            <div class="progress" style="height: 20px;">
                <div class="progress-bar" style="width: ${prob}%"></div>
            </div>
        </div>
    `).join('');
    
    document.getElementById('probabilitiesContainer').innerHTML = probsHtml;
    document.getElementById('processingTime').textContent = data.processing_time;
    document.getElementById('resultsContainer').style.display = 'block';
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorContainer').style.display = 'block';
}
