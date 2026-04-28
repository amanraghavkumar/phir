from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import time
from datetime import datetime

# Import custom modules
from config import config
from models.medical_classifier import MedicalClassifier
from utils.preprocessing import ImagePreprocessor, ImageValidator
from utils.helpers import Logger, FileManager, ResponseFormatter

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(config['development'])

# Enable CORS
CORS(app)

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)

# Initialize components
logger = Logger(app.config['LOG_FOLDER'])
file_manager = FileManager()
preprocessor = ImagePreprocessor(img_size=app.config['IMG_SIZE'])
validator = ImageValidator(app.config['ALLOWED_EXTENSIONS'], app.config['MAX_CONTENT_LENGTH'])

# Load model
try:
    classifier = MedicalClassifier(
        app.config['MODEL_PATH'],
        class_names=app.config['CLASSES']
    )
    logger.log_info("Model loaded successfully")
except Exception as e:
    classifier = None
    logger.log_error(f"Failed to load model: {str(e)}")

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', classes=app.config['CLASSES'])

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'model_loaded': classifier is not None and classifier.is_loaded,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/info', methods=['GET'])
def model_info():
    """Get model information"""
    if classifier and classifier.is_loaded:
        info = classifier.get_model_info()
        return jsonify(ResponseFormatter.success(info, "Model information"))
    else:
        return jsonify(ResponseFormatter.error("Model not loaded", 503)), 503

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    start_time = time.time()
    
    try:
        # Check if model is loaded
        if not classifier or not classifier.is_loaded:
            return jsonify(ResponseFormatter.error("Model not loaded", 503)), 503
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify(ResponseFormatter.error("No file provided", 400)), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify(ResponseFormatter.error("No file selected", 400)), 400
        
        # Validate file
        is_valid, errors = validator.validate_file(file)
        if not is_valid:
            return jsonify(ResponseFormatter.error("; ".join(errors), 400)), 400
        
        # Save uploaded file
        file_path = file_manager.save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
        
        # Preprocess image
        preprocessed_img = preprocessor.process_full_pipeline(file_path)
        
        # Make prediction
        result = classifier.predict(preprocessed_img)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Log prediction
        logger.log_prediction(
            file.filename,
            result['class'],
            result['confidence'],
            processing_time
        )
        
        # Return response
        response = ResponseFormatter.prediction_response(
            result['class'],
            result['confidence'],
            result['probabilities'],
            processing_time
        )
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.log_error(f"Prediction error: {str(e)}")
        return jsonify(ResponseFormatter.error(str(e), 500)), 500

@app.route('/predict-batch', methods=['POST'])
def predict_batch():
    """Batch prediction endpoint"""
    try:
        if not classifier or not classifier.is_loaded:
            return jsonify(ResponseFormatter.error("Model not loaded", 503)), 503
        
        if 'files' not in request.files:
            return jsonify(ResponseFormatter.error("No files provided", 400)), 400
        
        files = request.files.getlist('files')
        results = []
        
        for file in files:
            try:
                # Validate
                is_valid, errors = validator.validate_file(file)
                if not is_valid:
                    results.append({
                        'filename': file.filename,
                        'success': False,
                        'error': "; ".join(errors)
                    })
                    continue
                
                # Save and predict
                file_path = file_manager.save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
                preprocessed_img = preprocessor.process_full_pipeline(file_path)
                result = classifier.predict(preprocessed_img)
                
                results.append({
                    'filename': file.filename,
                    'success': True,
                    'predicted_class': result['class'],
                    'confidence': round(result['confidence'], 2),
                    'probabilities': result['probabilities']
                })
            except Exception as e:
                results.append({
                    'filename': file.filename,
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify(ResponseFormatter.success(results, "Batch prediction complete")), 200
    
    except Exception as e:
        return jsonify(ResponseFormatter.error(str(e), 500)), 500

@app.route('/upload', methods=['GET'])
def upload_page():
    """Upload page"""
    return render_template('predict.html', classes=app.config['CLASSES'])

@app.route('/classes', methods=['GET'])
def get_classes():
    """Get available classes"""
    return jsonify({
        'classes': app.config['CLASSES'],
        'num_classes': len(app.config['CLASSES'])
    }), 200

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify(ResponseFormatter.error("Resource not found", 404)), 404

@app.errorhandler(500)
def internal_error(error):
    logger.log_error(f"Internal error: {str(error)}")
    return jsonify(ResponseFormatter.error("Internal server error", 500)), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify(ResponseFormatter.error("File too large", 413)), 413

# ============================================================================
# STARTUP & SHUTDOWN
# ============================================================================

@app.before_request
def before_request():
    """Before each request"""
    pass

@app.after_request
def after_request(response):
    """After each request"""
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == '__main__':
    logger.log_info("Starting PHIR Medical Image Classification System")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
