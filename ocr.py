import pytesseract
import cv2
import numpy as np
from PIL import Image
import streamlit as st
import os
import json
import re

class TextExtractor:
    """Extracts handwritten text from UI sketches using OCR with enhanced preprocessing."""
    
    def __init__(self):
        # Multiple OCR configurations for different text types
        self.ocr_configs = [
            # Configuration optimized for handwritten text
            '--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?@#$%&*()_+-=[]{}|;:,.<>?/ ',
            # Configuration for single line text
            '--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?@#$%&*()_+-=[]{}|;:,.<>?/ ',
            # Configuration for sparse text
            '--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?@#$%&*()_+-=[]{}|;:,.<>?/ ',
            # Configuration for single word
            '--oem 3 --psm 13 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?@#$%&*()_+-=[]{}|;:,.<>?/ '
        ]
        self.setup_tesseract()
    
    def setup_tesseract(self):
        """Sets up Tesseract OCR configuration."""
        try:
            # Try to set Tesseract path for different OS
            if os.name == 'nt':  # Windows
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            # For macOS and Linux, assume tesseract is in PATH
            
            # Test tesseract
            version = pytesseract.get_tesseract_version()
            st.success(f"✅ Tesseract OCR {version} loaded successfully")
        except Exception as e:
            st.error(f"❌ Error setting up Tesseract: {str(e)}")
            st.info("Please install Tesseract OCR: https://github.com/tesseract-ocr/tesseract")
    
    def preprocess_for_ocr(self, image):
        """
        Enhanced preprocessing specifically for handwritten text OCR.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            List of preprocessed images with different techniques
        """
        # Convert PIL to numpy if needed
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image.copy()
        
        # Convert to grayscale if needed
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        processed_images = []
        
        # Technique 1: Standard preprocessing
        processed1 = self._standard_preprocessing(gray)
        processed_images.append(processed1)
        
        # Technique 2: High contrast preprocessing
        processed2 = self._high_contrast_preprocessing(gray)
        processed_images.append(processed2)
        
        # Technique 3: Noise reduction preprocessing
        processed3 = self._noise_reduction_preprocessing(gray)
        processed_images.append(processed3)
        
        # Technique 4: Edge enhancement preprocessing
        processed4 = self._edge_enhancement_preprocessing(gray)
        processed_images.append(processed4)
        
        return processed_images
    
    def _standard_preprocessing(self, gray):
        """Standard preprocessing technique."""
        # Resize for better OCR
        height, width = gray.shape
        scale_factor = max(2.0, 800 / max(width, height))
        if scale_factor > 1.0:
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            resized = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        else:
            resized = gray
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(resized, (3, 3), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Invert colors
        inverted = cv2.bitwise_not(thresh)
        
        return inverted
    
    def _high_contrast_preprocessing(self, gray):
        """High contrast preprocessing technique."""
        # Resize
        height, width = gray.shape
        scale_factor = max(2.0, 800 / max(width, height))
        if scale_factor > 1.0:
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            resized = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        else:
            resized = gray
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(resized)
        
        # Apply Otsu thresholding
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Invert colors
        inverted = cv2.bitwise_not(thresh)
        
        return inverted
    
    def _noise_reduction_preprocessing(self, gray):
        """Noise reduction preprocessing technique."""
        # Resize
        height, width = gray.shape
        scale_factor = max(2.0, 800 / max(width, height))
        if scale_factor > 1.0:
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            resized = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        else:
            resized = gray
        
        # Apply bilateral filter to reduce noise while preserving edges
        denoised = cv2.bilateralFilter(resized, 9, 75, 75)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 5
        )
        
        # Invert colors
        inverted = cv2.bitwise_not(thresh)
        
        return inverted
    
    def _edge_enhancement_preprocessing(self, gray):
        """Edge enhancement preprocessing technique."""
        # Resize
        height, width = gray.shape
        scale_factor = max(2.0, 800 / max(width, height))
        if scale_factor > 1.0:
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            resized = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        else:
            resized = gray
        
        # Apply unsharp mask for edge enhancement
        gaussian = cv2.GaussianBlur(resized, (0, 0), 2.0)
        enhanced = cv2.addWeighted(resized, 1.5, gaussian, -0.5, 0)
        
        # Apply thresholding
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Invert colors
        inverted = cv2.bitwise_not(thresh)
        
        return inverted
    
    def extract_text_from_region(self, image, bbox):
        """
        Extracts text from a specific region using multiple OCR attempts.
        
        Args:
            image: PIL Image or numpy array
            bbox: Bounding box [x1, y1, x2, y2]
            
        Returns:
            Extracted text string with highest confidence
        """
        try:
            # Crop the region
            x1, y1, x2, y2 = bbox
            cropped = image.crop((x1, y1, x2, y2)) if isinstance(image, Image.Image) else image[y1:y2, x1:x2]
            
            # Get multiple preprocessed versions
            processed_images = self.preprocess_for_ocr(cropped)
            
            best_text = ""
            best_confidence = 0
            
            # Try OCR with different configurations and preprocessing
            for i, processed_img in enumerate(processed_images):
                for j, config in enumerate(self.ocr_configs):
                    try:
                        text = pytesseract.image_to_string(
                            processed_img, 
                            config=config,
                            lang='eng'
                        )
                        
                        # Get confidence score
                        data = pytesseract.image_to_data(
                            processed_img,
                            config=config,
                            lang='eng',
                            output_type=pytesseract.Output.DICT
                        )
                        
                        # Calculate average confidence
                        confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
                        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                        
                        # Clean the text
                        cleaned_text = self.clean_text(text)
                        
                        # Update best result if confidence is higher
                        if cleaned_text and avg_confidence > best_confidence:
                            best_text = cleaned_text
                            best_confidence = avg_confidence
                            
                    except Exception as e:
                        continue
            
            return best_text
            
        except Exception as e:
            st.warning(f"OCR failed for region {bbox}: {str(e)}")
            return ""
    
    def extract_text_from_image(self, image):
        """
        Extracts all text from the entire image using multiple techniques.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            List of text regions with their bounding boxes
        """
        try:
            # Get multiple preprocessed versions
            processed_images = self.preprocess_for_ocr(image)
            
            all_text_regions = []
            
            # Try OCR with different preprocessing and configurations
            for i, processed_img in enumerate(processed_images):
                for j, config in enumerate(self.ocr_configs):
                    try:
                        # Get text with bounding boxes
                        data = pytesseract.image_to_data(
                            processed_img, 
                            config=config,
                            lang='eng',
                            output_type=pytesseract.Output.DICT
                        )
                        
                        for k in range(len(data['text'])):
                            # Filter out empty text and low confidence
                            text = data['text'][k].strip()
                            conf = int(data['conf'][k])
                            
                            if text and conf > 20:  # Lower confidence threshold for handwritten text
                                x = data['left'][k]
                                y = data['top'][k]
                                w = data['width'][k]
                                h = data['height'][k]
                                
                                # Clean the text
                                cleaned_text = self.clean_text(text)
                                
                                if cleaned_text:
                                    # Check if this region overlaps with existing ones
                                    new_bbox = [x, y, x + w, y + h]
                                    is_duplicate = False
                                    
                                    for existing_region in all_text_regions:
                                        if self._bbox_overlap(new_bbox, existing_region['bbox']):
                                            # Keep the one with higher confidence
                                            if conf > existing_region['confidence'] * 100:
                                                existing_region['text'] = cleaned_text
                                                existing_region['confidence'] = conf / 100.0
                                                existing_region['bbox'] = new_bbox
                                                existing_region['center'] = [x + w // 2, y + h // 2]
                                            is_duplicate = True
                                            break
                                    
                                    if not is_duplicate:
                                        all_text_regions.append({
                                            'text': cleaned_text,
                                            'bbox': new_bbox,
                                            'confidence': conf / 100.0,
                                            'center': [x + w // 2, y + h // 2]
                                        })
                                        
                    except Exception as e:
                        continue
            
            return all_text_regions
            
        except Exception as e:
            st.error(f"OCR extraction failed: {str(e)}")
            return []
    
    def _bbox_overlap(self, bbox1, bbox2, threshold=0.5):
        """Check if two bounding boxes overlap significantly."""
        x1_1, y1_1, x2_1, y2_1 = bbox1
        x1_2, y1_2, x2_2, y2_2 = bbox2
        
        # Calculate intersection
        x1_i = max(x1_1, x1_2)
        y1_i = max(y1_1, y1_2)
        x2_i = min(x2_1, x2_2)
        y2_i = min(y2_1, y2_2)
        
        if x2_i <= x1_i or y2_i <= y1_i:
            return False
        
        intersection = (x2_i - x1_i) * (y2_i - y1_i)
        area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
        area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
        
        # Calculate overlap ratio
        overlap_ratio = intersection / min(area1, area2)
        
        return overlap_ratio > threshold
    
    def clean_text(self, text):
        """
        Enhanced text cleaning for handwritten text.
        
        Args:
            text: Raw OCR text
            
        Returns:
            Cleaned text string
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters that are likely OCR errors
        text = re.sub(r'[^\w\s.,!?@#$%&*()_+\-=\[\]{}|;:,.<>?/]', '', text)
        
        # Enhanced normalization for handwritten text
        replacements = {
            # Common handwritten OCR mistakes
            '0': 'o', '1': 'l', '5': 's', '8': 'B', '6': 'G', '9': 'g',
            '2': 'Z', '3': 'E', '4': 'A', '7': 'T',
            # Lowercase to uppercase for common UI elements
            'submit': 'Submit', 'login': 'Login', 'signup': 'Signup',
            'username': 'Username', 'password': 'Password', 'email': 'Email',
            'name': 'Name', 'phone': 'Phone', 'address': 'Address',
            'search': 'Search', 'cancel': 'Cancel', 'save': 'Save',
            'delete': 'Delete', 'edit': 'Edit', 'add': 'Add',
            'next': 'Next', 'back': 'Back', 'continue': 'Continue',
            'home': 'Home', 'menu': 'Menu', 'settings': 'Settings',
            'profile': 'Profile', 'logout': 'Logout', 'register': 'Register'
        }
        
        # Apply replacements
        for wrong, correct in replacements.items():
            text = text.replace(wrong, correct)
        
        # Capitalize first letter of each word for UI elements
        words = text.split()
        capitalized_words = []
        for word in words:
            if len(word) > 1 and word.lower() in ['button', 'input', 'label', 'form', 'card', 'modal', 'nav', 'header', 'footer']:
                capitalized_words.append(word.capitalize())
            else:
                capitalized_words.append(word)
        
        text = ' '.join(capitalized_words)
        
        return text
    
    def extract_text_from_elements(self, image, detected_elements):
        """
        Extracts text from specific detected UI elements.
        
        Args:
            image: PIL Image or numpy array
            detected_elements: List of detected UI elements with bounding boxes
            
        Returns:
            List of elements with extracted text
        """
        elements_with_text = []
        
        for element in detected_elements:
            bbox = element['bbox']
            
            # Extract text from this region
            text = self.extract_text_from_region(image, bbox)
            
            # Add text to element
            element_with_text = element.copy()
            element_with_text['text'] = text
            
            elements_with_text.append(element_with_text)
        
        return elements_with_text
    
    def visualize_text_regions(self, image, text_regions):
        """
        Visualizes detected text regions on the image.
        
        Args:
            image: PIL Image or numpy array
            text_regions: List of text regions with bounding boxes
            
        Returns:
            Image with text regions highlighted
        """
        # Convert PIL to numpy if needed
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image.copy()
        
        # Convert to BGR for OpenCV
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
        
        # Draw bounding boxes for text regions
        for region in text_regions:
            bbox = region['bbox']
            text = region['text']
            confidence = region['confidence']
            
            # Draw rectangle
            cv2.rectangle(img_bgr, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
            
            # Add text label
            label = f"'{text}': {confidence:.2f}"
            cv2.putText(img_bgr, label, (bbox[0], bbox[1] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
        
        # Convert back to RGB for display
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        return Image.fromarray(img_rgb)
    
    def save_text_results(self, text_regions, filename="text_extraction.json"):
        """
        Saves text extraction results to a JSON file.
        
        Args:
            text_regions: List of text regions
            filename: Name of the output file
        """
        os.makedirs("temp", exist_ok=True)
        file_path = os.path.join("temp", filename)
        
        with open(file_path, 'w') as f:
            json.dump(text_regions, f, indent=2)
        
        return file_path

    def get_ocr_feedback(self, image):
        """
        Provides detailed feedback about OCR performance and suggestions.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Dictionary with OCR feedback and suggestions
        """
        try:
            # Get text regions
            text_regions = self.extract_text_from_image(image)
            
            # Analyze results
            total_regions = len(text_regions)
            high_confidence = len([r for r in text_regions if r['confidence'] > 0.7])
            medium_confidence = len([r for r in text_regions if 0.4 <= r['confidence'] <= 0.7])
            low_confidence = len([r for r in text_regions if r['confidence'] < 0.4])
            
            # Calculate average confidence
            avg_confidence = sum(r['confidence'] for r in text_regions) / total_regions if total_regions > 0 else 0
            
            # Generate suggestions
            suggestions = []
            if total_regions == 0:
                suggestions.append("No text detected. Try improving image quality or contrast.")
            elif low_confidence > high_confidence:
                suggestions.append("Many low-confidence detections. Consider redrawing text more clearly.")
            elif avg_confidence < 0.5:
                suggestions.append("Overall low confidence. Try using darker pen or better lighting.")
            
            if total_regions > 0:
                suggestions.append(f"Detected {total_regions} text regions with {avg_confidence:.1%} average confidence.")
            
            return {
                'total_regions': total_regions,
                'high_confidence': high_confidence,
                'medium_confidence': medium_confidence,
                'low_confidence': low_confidence,
                'average_confidence': avg_confidence,
                'suggestions': suggestions,
                'detected_texts': [r['text'] for r in text_regions]
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'suggestions': ["OCR processing failed. Check if Tesseract is properly installed."]
            }
    
    def extract_text_with_fallback(self, image, bbox=None):
        """
        Extracts text with multiple fallback strategies.
        
        Args:
            image: PIL Image or numpy array
            bbox: Optional bounding box [x1, y1, x2, y2]
            
        Returns:
            Best text result with confidence score
        """
        if bbox:
            # Extract from specific region
            return self.extract_text_from_region(image, bbox)
        else:
            # Extract from entire image
            text_regions = self.extract_text_from_image(image)
            
            if not text_regions:
                return ""
            
            # Return the text with highest confidence
            best_region = max(text_regions, key=lambda x: x['confidence'])
            return best_region['text']

# Example usage
if __name__ == "__main__":
    extractor = TextExtractor()
    
    # Create a test image with text
    test_image = np.zeros((200, 400, 3), dtype=np.uint8)
    test_image.fill(255)  # White background
    
    # Add some test text (this would normally be handwritten)
    cv2.putText(test_image, "Submit", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(test_image, "Username", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Convert to PIL
    pil_image = Image.fromarray(test_image)
    
    # Extract text
    text_regions = extractor.extract_text_from_image(pil_image)
    print(f"Extracted {len(text_regions)} text regions:")
    for region in text_regions:
        print(f"- '{region['text']}': {region['bbox']} (conf: {region['confidence']:.2f})") 