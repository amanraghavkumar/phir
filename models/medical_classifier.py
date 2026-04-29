

import numpy as np
import os
import warnings
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model

warnings.filterwarnings('ignore')

original_dense_init = Dense.__init__
def patched_dense_init(self, *args, **kwargs):
    kwargs.pop('quantization_config', None) # Chupchap ise hata do agar mile
    original_dense_init(self, *args, **kwargs)
Dense.__init__ = patched_dense_init

class MedicalClassifier:
    def __init__(self, model_path, class_names=None):
        self.model_path = model_path
        self.class_names = class_names or [
            'Atelectasis', 'Effusion', 'Infiltration', 'No_Finding', 'Pneumonia'
        ]
        
        try:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file nahi mili: {model_path}")

            # Sab kuch bypass karke load karo
            self.model = load_model(model_path, compile=False)
            self.is_loaded = True
            print("\n" + "="*40)
            print("--- [SUCCESS] AB CHAL GAYA! MODEL LOADED ---")
            print("="*40 + "\n")
            
        except Exception as e:
            print(f"--- [STILL ERROR] Last Attempting Alternative... ---")
            try:
                # Agar h5 format ka lafda hai toh
                self.model = tf.keras.models.load_model(model_path, compile=False, custom_objects={'Dense': Dense})
                self.is_loaded = True
            except Exception as e2:
                print(f"FATAL ERROR: {str(e2)}")
                self.is_loaded = False
                self.model = None

    def predict(self, preprocessed_image):
        if not self.is_loaded or self.model is None:
            raise RuntimeError("Model load nahi hua hai.")
        
        if len(preprocessed_image.shape) == 3:
            preprocessed_image = np.expand_dims(preprocessed_image, axis=0)
            
        predictions = self.model.predict(preprocessed_image, verbose=0)
        prediction_probs = predictions[0]
        predicted_idx = np.argmax(prediction_probs)
        
        return {
            'class': self.class_names[predicted_idx],
            'confidence': float(prediction_probs[predicted_idx] * 100),
            'probabilities': {name: float(p * 100) for name, p in zip(self.class_names, prediction_probs)}
        }

    def get_model_info(self):
        return {'is_loaded': self.is_loaded, 'engine': 'Forced-Patch-TF'}