import os
import json
import logging
from datetime import datetime
from functools import wraps
import time

class Logger:
    """Application logger"""
    
    def __init__(self, log_folder):
        self.log_folder = log_folder
        os.makedirs(log_folder, exist_ok=True)
        
        # Setup logger
        self.logger = logging.getLogger('PHIR')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(os.path.join(log_folder, 'predictions.log'))
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    
    def log_prediction(self, filename, predicted_class, confidence, processing_time):
        """Log prediction"""
        self.logger.info(
            f"File: {filename} | Predicted: {predicted_class} | "
            f"Confidence: {confidence:.2f}% | Time: {processing_time:.3f}s"
        )
    
    def log_error(self, error_msg):
        """Log error"""
        self.logger.error(error_msg)
    
    def log_info(self, msg):
        """Log info"""
        self.logger.info(msg)

def timing_decorator(func):
    """Decorator to time function execution"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        return result, elapsed_time
    return wrapper

class FileManager:
    """File management utilities"""
    
    @staticmethod
    def save_uploaded_file(file, upload_folder):
        """Save uploaded file"""
        os.makedirs(upload_folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filepath
    
    @staticmethod
    def cleanup_old_files(upload_folder, days=1):
        """Remove files older than N days"""
        import glob
        from pathlib import Path
        
        now = time.time()
        cutoff = now - (days * 86400)
        
        for file_path in glob.glob(os.path.join(upload_folder, '*')):
            if os.path.isfile(file_path):
                if os.stat(file_path).st_mtime < cutoff:
                    try:
                        os.remove(file_path)
                    except:
                        pass

class ResponseFormatter:
    """API response formatting"""
    
    @staticmethod
    def success(data, message="Success"):
        return {
            'success': True,
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def error(error_msg, error_code=400):
        return {
            'success': False,
            'error': error_msg,
            'error_code': error_code,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def prediction_response(predicted_class, confidence, probabilities, processing_time):
        return {
            'success': True,
            'predicted_class': predicted_class,
            'confidence': round(confidence, 2),
            'probabilities': {
                class_name: round(prob, 4) 
                for class_name, prob in probabilities.items()
            },
            'processing_time': round(processing_time, 3),
            'timestamp': datetime.now().isoformat()
        }
