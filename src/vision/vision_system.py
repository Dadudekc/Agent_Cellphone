import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image, ImageGrab
import time
import json
from typing import Dict, List, Tuple, Optional
import logging

class VisionSystem:
    """
    Vision system for AI agents to "see" what's on screen
    Provides screenshot capture, OCR, and visual analysis capabilities
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize OCR engine
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            self.logger.warning(f"Tesseract not found: {e}")
        
        # Screen capture settings
        self.capture_region = self.config.get('capture_region', None)  # (x, y, width, height)
        self.capture_frequency = self.config.get('capture_frequency', 1.0)  # seconds
        
    def capture_screen(self, region: Tuple[int, int, int, int] = None) -> np.ndarray:
        """
        Capture screenshot of specified region or full screen
        """
        try:
            if region:
                screenshot = ImageGrab.grab(bbox=region)
            else:
                screenshot = ImageGrab.grab()
            
            # Convert to numpy array
            img_array = np.array(screenshot)
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            self.logger.info(f"Screenshot captured: {img_array.shape}")
            return img_array
            
        except Exception as e:
            self.logger.error(f"Screen capture failed: {e}")
            return None
    
    def extract_text(self, image: np.ndarray) -> str:
        """
        Extract text from image using OCR
        """
        try:
            # Convert to grayscale for better OCR
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply preprocessing for better text recognition
            # Remove noise
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Apply threshold
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Extract text
            text = pytesseract.image_to_string(thresh)
            
            self.logger.info(f"Text extracted: {len(text)} characters")
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"OCR failed: {e}")
            return ""
    
    def detect_ui_elements(self, image: np.ndarray) -> List[Dict]:
        """
        Detect UI elements like buttons, text fields, etc.
        """
        ui_elements = []
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect rectangles (potential buttons/fields)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Approximate contour to polygon
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Filter by area and shape
                area = cv2.contourArea(contour)
                if area > 100:  # Minimum area threshold
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    ui_elements.append({
                        'type': 'rectangle',
                        'position': (x, y),
                        'size': (w, h),
                        'area': area,
                        'corners': len(approx)
                    })
            
            self.logger.info(f"Detected {len(ui_elements)} UI elements")
            return ui_elements
            
        except Exception as e:
            self.logger.error(f"UI detection failed: {e}")
            return []
    
    def find_text_regions(self, image: np.ndarray) -> List[Dict]:
        """
        Find regions containing text
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Use Tesseract to get text regions
            data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
            
            text_regions = []
            for i, text in enumerate(data['text']):
                if text.strip():  # Only non-empty text
                    x = data['left'][i]
                    y = data['top'][i]
                    w = data['width'][i]
                    h = data['height'][i]
                    conf = data['conf'][i]
                    
                    text_regions.append({
                        'text': text,
                        'position': (x, y),
                        'size': (w, h),
                        'confidence': conf
                    })
            
            self.logger.info(f"Found {len(text_regions)} text regions")
            return text_regions
            
        except Exception as e:
            self.logger.error(f"Text region detection failed: {e}")
            return []
    
    def analyze_screen_content(self, image: np.ndarray) -> Dict:
        """
        Comprehensive screen analysis
        """
        analysis = {
            'timestamp': time.time(),
            'image_shape': image.shape,
            'text_content': self.extract_text(image),
            'ui_elements': self.detect_ui_elements(image),
            'text_regions': self.find_text_regions(image)
        }
        
        return analysis
    
    def continuous_monitoring(self, callback_func, duration: int = None):
        """
        Continuously monitor screen and call callback with analysis
        """
        start_time = time.time()
        
        while True:
            if duration and (time.time() - start_time) > duration:
                break
                
            # Capture screen
            image = self.capture_screen(self.capture_region)
            if image is not None:
                # Analyze content
                analysis = self.analyze_screen_content(image)
                
                # Call callback with analysis
                callback_func(analysis)
            
            # Wait before next capture
            time.sleep(self.capture_frequency)
    
    def save_vision_data(self, analysis: Dict, filename: str):
        """
        Save vision analysis data to file
        """
        try:
            with open(filename, 'w') as f:
                json.dump(analysis, f, indent=2)
            self.logger.info(f"Vision data saved to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to save vision data: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize vision system
    vision = VisionSystem()
    
    # Capture and analyze screen
    image = vision.capture_screen()
    if image is not None:
        analysis = vision.analyze_screen_content(image)
        print("Screen Analysis:", json.dumps(analysis, indent=2)) 