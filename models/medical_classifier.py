import numpy as np
from tensorflow import keras
import warnings

warnings.filterwarnings('ignore')

class MedicalClassifier:
    """Wrapper class for medical image classification model"""
    
    def __init__(self, model_path, class_names=None):
        """
        Initialize classifier
        
        Args:
            model_path (str): Path to trained model
            class_names (list): List of class names
        """
        self.model_path = model_path
        self.class_names = class_names or [
            'Atelectasis',
            'Effusion',
            'Infiltration',
            'No_Finding',
            'Pneumonia'
        ]
        
        try:
            self.model = keras.models.load_model(model_path)
            self.is_loaded = True
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.is_loaded = False
            self.model = None
    
    def predict(self, preprocessed_image):
        """
        Make prediction on preprocessed image
        
        Args:
            preprocessed_image (np.ndarray): Preprocessed image array
            
        Returns:
            dict: Prediction results with class, confidence, and probabilities
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")
        
        try:
            # Predict
            predictions = self.model.predict(preprocessed_image, verbose=0)
            prediction_probs = predictions[0]
            
            # Get predicted class
            predicted_idx = np.argmax(prediction_probs)
            predicted_class = self.class_names[predicted_idx]
            confidence = float(prediction_probs[predicted_idx] * 100)
            
            # Probabilities for all classes
            probabilities = {
                class_name: float(prob * 100)
                for class_name, prob in zip(self.class_names, prediction_probs)
            }
            
            return {
                'class': predicted_class,
                'confidence': confidence,
                'probabilities': probabilities,
                'predictions_array': prediction_probs
            }
        except Exception as e:
            raise RuntimeError(f"Prediction error: {str(e)}")
    
    def predict_batch(self, preprocessed_images):
        """
        Make batch predictions
        
        Args:
            preprocessed_images (np.ndarray): Batch of preprocessed images
            
        Returns:
            list: List of prediction dictionaries
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")
        
        try:
            predictions = self.model.predict(preprocessed_images, verbose=0)
            results = []
            
            for pred_probs in predictions:
                predicted_idx = np.argmax(pred_probs)
                predicted_class = self.class_names[predicted_idx]
                confidence = float(pred_probs[predicted_idx] * 100)
                
                results.append({
                    'class': predicted_class,
                    'confidence': confidence,
                    'probabilities': {
                        class_name: float(prob * 100)
                        for class_name, prob in zip(self.class_names, pred_probs)
                    }
                })
            
            return results
        except Exception as e:
            raise RuntimeError(f"Batch prediction error: {str(e)}")
    
    def get_model_info(self):
        """
        Get model information
        
        Returns:
            dict: Model information
        """
        if not self.is_loaded:
            return None
        
        return {
            'model_path': self.model_path,
            'is_loaded': self.is_loaded,
            'classes': self.class_names,
            'num_classes': len(self.class_names),
            'model_type': type(self.model).__name__
        }
