import cv2
import numpy as np
import albumentations as A
from PIL import Image
from io import BytesIO

class ImagePreprocessor:
    """Image preprocessing and normalization"""
    
    def __init__(self, img_size=384):
        self.img_size = img_size
        
        # Normalization transform
        self.transform = A.Compose([
            A.Normalize(mean=[0.485, 0.456, 0.406], 
                       std=[0.229, 0.224, 0.225]),
        ])
    
    def load_image(self, image_path):
        """Load image from file path"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not load image")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img
        except Exception as e:
            raise ValueError(f"Image loading error: {str(e)}")
    
    def load_image_from_bytes(self, image_bytes):
        """Load image from bytes (file upload)"""
        try:
            img = Image.open(BytesIO(image_bytes)).convert('RGB')
            img = np.array(img)
            return img
        except Exception as e:
            raise ValueError(f"Image conversion error: {str(e)}")
    
    def preprocess(self, image):
        """Preprocess image for model"""
        try:
            # Resize
            img = cv2.resize(image, (self.img_size, self.img_size))
            
            # Normalize
            augmented = self.transform(image=img)
            img = augmented['image']
            
            # Add batch dimension
            img = np.expand_dims(img, axis=0)
            
            return img.astype(np.float32)
        except Exception as e:
            raise ValueError(f"Preprocessing error: {str(e)}")
    
    def process_full_pipeline(self, image_path):
        """Full pipeline: load → preprocess"""
        img = self.load_image(image_path)
        img = cv2.resize(img, (self.img_size, self.img_size))
        processed = self.preprocess(img)
        return processed

class ImageValidator:
    """Validate uploaded images"""
    
    def __init__(self, allowed_extensions, max_size):
        self.allowed_extensions = allowed_extensions
        self.max_size = max_size
    
    def validate_extension(self, filename):
        """Check file extension"""
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        return ext in self.allowed_extensions
    
    def validate_size(self, file_size):
        """Check file size"""
        return file_size <= self.max_size
    
    def validate_image(self, image_bytes):
        """Check if valid image"""
        try:
            img = Image.open(BytesIO(image_bytes))
            img.verify()
            return True
        except:
            return False
    
    def validate_file(self, file_obj):
        """Full validation"""
        errors = []
        
        if not self.validate_extension(file_obj.filename):
            errors.append('Invalid file extension. Allowed: ' + ', '.join(self.allowed_extensions))
        
        # Get file size
        file_obj.seek(0, 2)
        file_size = file_obj.tell()
        file_obj.seek(0)
        
        if not self.validate_size(file_size):
            errors.append(f'File too large. Maximum: {self.max_size / 1024 / 1024}MB')
        
        if not self.validate_image(file_obj.read()):
            errors.append('Invalid image file')
        
        file_obj.seek(0)
        
        return len(errors) == 0, errors
