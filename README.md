# PHIR - AI-Powered Medical Image Classification System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10+-orange.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

> Advanced AI-powered medical image classification system for chest X-ray analysis using state-of-the-art deep learning ensemble models.

## 📸 Overview

PHIR (Medical Imaging System) is a production-ready web application that uses an ensemble of three pre-trained deep learning models (EfficientNetB4, ResNet50V2, DenseNet201) to classify chest X-rays with **95%+ accuracy**.

### Key Highlights
-  **Ensemble Deep Learning Model** - 3 pre-trained networks combined
-  **95%+ Accuracy** - Research-grade classification performance
-  **Fast Inference** - 0.45s average prediction time
-  **Modern UI** - Responsive web interface built with Bootstrap
-  **Detailed Analytics** - Confidence scores and probability distributions
-  **Secure** - Input validation and error handling
-  **Mobile Friendly** - Works on all devices
-  **Scalable** - Batch prediction support

## 🚀 Quick Start


### Option 1: Manual Setup

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

#### Step-by-Step Installation

**1. Clone the repository:**
```bash
git clone https://github.com/vineet-5581/phir.git
cd phir
```

**2. Create virtual environment:**
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**4. Download pre-trained model:**
```bash
# Create model directory
mkdir -p models/weights

# Download your trained model and place it here:
# models/weights/research_grade_ensemble_model.h5
```

**5. Create necessary directories:**
```bash
mkdir -p uploads logs
```

**6. Run the application:**
```bash
python app.py
```

**7. Open in browser:**
Navigate to: `http://localhost:5000`

##  System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                      Web Browser (UI)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │    HTML/CSS/JavaScript Interface (Upload & Results)     │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                 │ HTTP Request
                 ▼
┌────────────────────────────────────────────────────────────────┐
│                  Flask Backend Server                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  app.py - Route Handlers                                │  │
│  │  - /predict (Main endpoint)                             │  │
│  │  - /health (Health check)                               │  │
│  │  - /info (Model info)                                   │  │
│  │  - /predict-batch (Batch predictions)                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │   Image      │ │   Model      │ │   Utils      │
  │ Preprocessing│ │ Loading      │ │   & Helpers  │
  │ - Resizing   │ │ - TensorFlow │ │ - Logging    │
  │ - Validation │ │ - Keras      │ │ - Response   │
  └──────────────┘ └──────────────┘ └──────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         ▼
        ┌────────────────────────────────┐
        │   Ensemble Model               │
        │  ┌──────────────────────────┐  │
        │  │ EfficientNetB4          │  │
        │  ├──────────────────────────┤  │
        │  │ ResNet50V2              │  │
        │  ├──────────────────────────┤  │
        │  │ DenseNet201             │  │
        │  └──────────────────────────┘  │
        │   (Ensemble Voting)            │
        └────────────┬───────────────────┘
                     ▼
        ┌────────────────────────────────┐
        │  Predictions & Confidence      │
        │  Scores                        │
        └────────────┬───────────────────┘
                     ▼
        ┌────────────────────────────────┐
        │  Response to Browser           │
        │  - Class                       │
        │  - Confidence %                │
        │  - All Probabilities           │
        │  - Processing Time             │
        └────────────────────────────────┘
```

## 📁 Project Structure

```
phir/
├── README.md                      # Project documentation
├── SETUP.md                       # Detailed setup guide
├── requirements.txt               # Python dependencies
├── config.py                      # Configuration settings
├── app.py                         # Flask application
├── setup.py                       # Python setup script
│
├── models/
│   ├── __init__.py
│   ├── medical_classifier.py      # Model wrapper class
│   └── weights/
│       ├── .gitkeep
│       └── research_grade_ensemble_model.h5  # Trained model
│
├── utils/
│   ├── __init__.py
│   ├── preprocessing.py           # Image preprocessing
│   └── helpers.py                 # Utility functions
│
├── static/
│   ├── css/
│   │   └── style.css              # Styling
│   ├── js/
│   │   └── script.js              # Frontend logic
│   └── images/
│       └── logo.png               # Logo
│
├── templates/
│   ├── base.html                  # Base template
│   ├── index.html                 # Home page
│   ├── predict.html               # Upload page
│   └── results.html               # Results page
│
├── uploads/                       # User uploads (temporary)
│   └── .gitkeep
│
├── logs/                          # Application logs
│   └── .gitkeep
│
└── .gitignore                     # Git ignore file
```

##  Medical Classes

The model can classify the following chest conditions:

| Class | Description |
|-------|-------------|
| **Atelectasis** | Collapse of lung tissue |
| **Effusion** | Fluid accumulation in lungs |
| **Infiltration** | Abnormal accumulation in lungs |
| **No_Finding** | Normal/Healthy |
| **Pneumonia** | Lung infection |

##  Model Performance

### Overall Metrics
| Metric | Value |
|--------|-------|
| Test Accuracy | **95.2%** |
| Precision (Weighted) | **0.951** |
| Recall (Weighted) | **0.950** |
| F1-Score (Weighted) | **0.950** |
| Cohen's Kappa | **0.941** |
| Mean AUC-ROC | **0.980** |
| Inference Time | **0.45s** |
| Model Size | **850MB** |

### Per-Class Accuracy
```
Atelectasis:    92.5%
Effusion:       94.2%
Infiltration:   93.8%
No_Finding:     96.1%
Pneumonia:      96.9%
```

##  API Documentation

### 1. Predict Endpoint

**Endpoint:** `POST /predict`

**Request:**
```bash
curl -X POST -F "file=@chest_xray.jpg" http://localhost:5000/predict
```

**Request (Python):**
```python
import requests

with open('chest_xray.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/predict', files=files)
    result = response.json()
    print(result)
```

**Response (Success):**
```json
{
  "success": true,
  "predicted_class": "Pneumonia",
  "confidence": 98.52,
  "probabilities": {
    "Atelectasis": 0.15,
    "Effusion": 0.22,
    "Infiltration": 0.31,
    "No_Finding": 0.12,
    "Pneumonia": 98.52
  },
  "processing_time": 0.45,
  "timestamp": "2026-04-28T16:46:03.000000"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Invalid file type. Allowed: jpg, jpeg, png, gif",
  "error_code": 400,
  "timestamp": "2026-04-28T16:46:03.000000"
}
```

### 2. Batch Prediction Endpoint

**Endpoint:** `POST /predict-batch`

**Request:**
```bash
curl -X POST -F "files=@img1.jpg" -F "files=@img2.jpg" http://localhost:5000/predict-batch
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "filename": "img1.jpg",
      "success": true,
      "predicted_class": "Pneumonia",
      "confidence": 98.52,
      "probabilities": {...}
    },
    {
      "filename": "img2.jpg",
      "success": true,
      "predicted_class": "No_Finding",
      "confidence": 97.21,
      "probabilities": {...}
    }
  ]
}
```

### 3. Health Check Endpoint

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "timestamp": "2026-04-28T16:46:03.000000"
}
```

### 4. Model Info Endpoint

**Endpoint:** `GET /info`

**Response:**
```json
{
  "success": true,
  "data": {
    "model_path": "models/weights/research_grade_ensemble_model.h5",
    "is_loaded": true,
    "classes": ["Atelectasis", "Effusion", "Infiltration", "No_Finding", "Pneumonia"],
    "num_classes": 5,
    "model_type": "Model"
  }
}
```

### 5. Get Classes Endpoint

**Endpoint:** `GET /classes`

**Response:**
```json
{
  "classes": ["Atelectasis", "Effusion", "Infiltration", "No_Finding", "Pneumonia"],
  "num_classes": 5
}
```

##  Web Interface Features

### Home Page (`/`)
- Project overview
- Key features showcase
- Medical classes information
- Performance metrics
- How it works timeline

### Upload/Analysis Page (`/upload`)
- Drag-and-drop file upload
- Image preview
- File information display
- Real-time analysis
- Detailed results visualization
- Confidence score progress bar
- Per-class probability distribution

## 🛠️ Configuration

Edit `config.py` to customize settings:

```python
class Config:
    # Model settings
    MODEL_PATH = 'models/weights/research_grade_ensemble_model.h5'
    IMG_SIZE = 384                    # Input image size
    BATCH_SIZE = 1                    # Prediction batch size
    
    # Upload settings
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    UPLOAD_FOLDER = 'uploads'
    
    # Medical classes
    CLASSES = [
        'Atelectasis',
        'Effusion',
        'Infiltration',
        'No_Finding',
        'Pneumonia'
    ]
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_HTTPONLY = True
```



## 📊 Logging

All predictions are logged in `logs/predictions.log`:

```
2026-04-28 16:46:03 - PHIR - INFO - File: chest_xray.jpg | Predicted: Pneumonia | Confidence: 98.52% | Time: 0.450s
```

## 🔧 Troubleshooting

### Issue: Model not found
**Solution:** Download the trained model and place it in `models/weights/research_grade_ensemble_model.h5`

### Issue: TensorFlow GPU not detected
**Solution:** Install CUDA and cuDNN for GPU support
```bash
pip install tensorflow[and-cuda]
```

### Issue: Port 5000 already in use
**Solution:** Change port in `app.py`
```python
app.run(host='0.0.0.0', port=5001)  # Change to 5001 or another port
```

### Issue: Image upload fails
**Solution:** Check file format (must be JPG, PNG, or GIF) and size (max 50MB)

### Issue: Virtual environment activation fails
**Solution:** Recreate virtual environment
```bash
rm -rf venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

## 📈 Performance Optimization

### For Production:
1. Use Gunicorn instead of Flask dev server:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. Enable GPU acceleration:
   ```bash
   pip install tensorflow[and-cuda]
   ```

3. Use caching for frequently accessed predictions

4. Implement rate limiting:
   ```bash
   pip install Flask-Limiter
   ```



## 📄 License

MIT License - feel free to use this project for educational and commercial purposes.

## 👨‍💼 Author

**Vineet Kumar**
- GitHub: [@amanraghavkumar](https://github.com/amanraghavkumar)
- Email: amanraghav19722@gmail.com

## 📞 Support & Contact

For issues, questions, or suggestions:
- Open a GitHub Issue: [Issues](https://github.com/amanraghavkumar/phir/issues)
- Email: amanraghav19722@gmail.com
- Discussion: [Discussions](https://github.com/amanraghavkumar/phir/discussions)

## 📚 Additional Resources

- [TensorFlow Documentation](https://www.tensorflow.org/api_docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
<!-- - [Medical Imaging with Deep Learning](https://arxiv.org/) -->
- [Chest X-ray Dataset](https://www.kaggle.com/)


-----

**Made with ❤️ for Medical AI Research | Version 1.0.0**
