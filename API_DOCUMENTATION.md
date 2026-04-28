
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
