# 📋 PHIR - Detailed Setup Guide

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Configuration](#configuration)
4. [Model Setup](#model-setup)
5. [Running the Application](#running-the-application)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11
- **CPU**: Intel i5 or equivalent
- **RAM**: 8GB (16GB recommended)
- **Storage**: 2GB free space (including model)
- **Python**: 3.8 or higher

### Software Dependencies
- Python 3.8+
- pip (Python package manager)
- Git
- Virtual Environment tool (venv)

---

## Installation Methods

### Method 1: Manual Step-by-Step Setup

#### Step 1: Clone Repository

```bash
git clone https://github.com/amanraghavkumar/phir.git
cd phir
```

#### Step 2: Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Step 3: Upgrade pip

```bash
pip install --upgrade pip setuptools wheel
```

#### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Installation time:** ~5-10 minutes (depending on internet speed)

#### Step 5: Create Directories

```bash
# Linux/macOS
mkdir -p models/weights uploads logs

# Windows (Command Prompt)
mkdir models\weights uploads logs

# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path models\weights, uploads, logs
```

#### Step 6: Download Pre-trained Model

Download the trained model file: `research_grade_ensemble_model.h5`

Place it in: `models/weights/research_grade_ensemble_model.h5`

#### Step 7: Verify Installation

```bash
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"
python -c "import flask; print('Flask version:', flask.__version__)"
```

#### Step 8: Run Application

```bash
python app.py
```

---

## Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# .env file
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
MODEL_PATH=models/weights/research_grade_ensemble_model.h5
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=52428800  # 50MB in bytes
```

### config.py Settings

**Development Environment:**
```python
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False
```

**Production Environment:**
```python
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
```

---

## Model Setup

### Downloading the Model

1. **Option A: Download from Cloud Storage**
   ```bash
   mkdir -p models/weights
   cd models/weights
   # Download file using gdown or similar tool
   ```

2. **Option B: Train Your Own Model**
   - Use the training code provided
   - Save model: `model.save('research_grade_ensemble_model.h5')`
   - Place in `models/weights/` directory

3. **Option C: Use Docker Image**
   - Pre-built image with model included
   - See Docker section

### Model Verification

```python
import tensorflow as tf

# Load model
model = tf.keras.models.load_model('models/weights/research_grade_ensemble_model.h5')

# Print model info
model.summary()
print(f"Model input shape: {model.input_shape}")
print(f"Model output shape: {model.output_shape}")
```

### Model Size
- **File Size**: ~850MB
- **RAM Required**: ~2GB
- **GPU Memory**: ~4GB (optional)

---

## Running the Application

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Run Flask app
python app.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**Access:** Open browser and go to `http://localhost:5000`

### Production Server with Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Run with specific configuration
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

### Production Server with uWSGI

```bash
# Install uWSGI
pip install uwsgi

# Run application
uwsgi --http :5000 --wsgi-file app.py --callable app --processes 4 --threads 2
```

### Background Process (Linux/macOS)

```bash
# Run in background
nohup python app.py > app.log 2>&1 &

# Check process
ps aux | grep app.py

# Kill process
kill -9 <PID>
```

---


## Troubleshooting

### Python & Dependencies

**Issue: Python command not found**
```bash
# Check Python installation
python --version

# Try python3
python3 --version

# Add to PATH (Windows)
# Search: Environment Variables → Edit System Environment Variables
```

**Issue: pip install fails**
```bash
# Upgrade pip
pip install --upgrade pip

# Try installing with specific version
pip install tensorflow==2.10.0

# Check internet connection
ping google.com
```

### Virtual Environment

**Issue: venv not activating**
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
```

**Issue: Module not found after installing**
```bash
# Verify virtual environment is active
which python  # Should show venv path

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Model Loading

**Issue: Model file not found**
```bash
# Check file exists
ls -la models/weights/

# Verify file size (should be ~850MB)
du -h models/weights/research_grade_ensemble_model.h5
```

**Issue: Model loading error**
```python
# Debug script
import tensorflow as tf
try:
    model = tf.keras.models.load_model('models/weights/research_grade_ensemble_model.h5')
    print("Model loaded successfully")
except Exception as e:
    print(f"Error: {e}")
```

### Application Errors

**Issue: Port 5000 already in use**
```bash
# Find process using port
lsof -i :5000  # Linux/macOS
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>  # Linux/macOS
taskkill /PID <PID> /F  # Windows

# Use different port
python app.py --port 5001
```

**Issue: CORS errors**
```python
# Already enabled in app.py with Flask-CORS
from flask_cors import CORS
CORS(app)
```

### GPU Support

**Check GPU availability:**
```python
import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))
```

**Install CUDA support:**
```bash
# For NVIDIA GPUs
pip install tensorflow[and-cuda]

# Verify CUDA is working
python -c "import tensorflow as tf; print(tf.sysconfig.get_build_info()['cuda_version'])"
```

---

## Performance Tips

1. **Use GPU**: Install CUDA for faster inference
2. **Enable Caching**: Cache frequent predictions
3. **Batch Processing**: Use `/predict-batch` for multiple images
4. **Production Server**: Use Gunicorn/uWSGI instead of Flask dev
5. **Load Balancing**: Use Nginx for multiple app instances

---

## Uninstallation

To completely remove PHIR:

```bash
# Remove virtual environment
rm -rf venv

# Remove project directory
cd ..
rm -rf phir

# Remove uploaded files (if needed)
rm -rf ~/phir_uploads
```

---

## Support

For issues or questions:
- GitHub Issues: [Create Issue](https://github.com/amanraghavkumar/phir/issues)
- Email: amanraghav19722@gmail.com
- Documentation: [README.md](README.md)

---

**Last Updated**: 2026-04-28  
**Version**: 1.0.0
