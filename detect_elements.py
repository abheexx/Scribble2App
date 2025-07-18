import cv2
import numpy as np
from ultralytics import YOLO
import streamlit as st
from PIL import Image
import os
import json

class UIElementDetector:
    """Uses YOLOv8 to detect UI elements in hand-drawn sketches."""
    
    def __init__(self):
        self.model = None
        self.class_names = [
            'button', 'input', 'text', 'image', 'checkbox', 
            'radio', 'dropdown', 'textarea', 'link', 'header',
            'footer', 'sidebar', 'card', 'modal', 'table'
        ]
        self.load_model()
    
    def load_model(self):
        """Loads the YOLOv8 model for UI element detection."""
        try:
            # For now, we'll use a pre-trained YOLOv8 model
            # In production, you'd want to train on UI sketch data
            self.model = YOLO('yolov8n.pt')
            st.success("✅ YOLOv8 model loaded successfully")
        except Exception as e:
            st.error(f"❌ Error loading YOLOv8 model: {str(e)}")
            # Fallback to basic contour detection
            self.model = None
    
    def detect_elements(self, image):
        """
        Detects UI elements in the image using enhanced fallback detection for hand-drawn sketches.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            List of detected elements with bounding boxes and confidence scores
        """
        # For hand-drawn sketches, prioritize fallback detection
        # YOLOv8 is trained on digital UI elements, not hand-drawn sketches
        try:
            # Try YOLOv8 first with very low confidence threshold
            if self.model is not None:
                # Convert PIL to numpy if needed
                if isinstance(image, Image.Image):
                    img_array = np.array(image)
                else:
                    img_array = image
                
                # Run YOLOv8 detection with very low confidence for hand-drawn sketches
                results = self.model(img_array, conf=0.1, iou=0.3)
                
                detected_elements = []
                
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            # Get bounding box coordinates
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            
                            # Get confidence score
                            confidence = box.conf[0].cpu().numpy()
                            
                            # Get class prediction
                            class_id = int(box.cls[0].cpu().numpy())
                            class_name = self.class_names[class_id] if class_id < len(self.class_names) else f"element_{class_id}"
                            
                            detected_elements.append({
                                'type': class_name,
                                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                                'confidence': float(confidence),
                                'center': [int((x1 + x2) / 2), int((y1 + y2) / 2)]
                            })
                
                # If YOLOv8 found elements with decent confidence, use them
                if detected_elements and any(elem['confidence'] > 0.3 for elem in detected_elements):
                    return detected_elements
        except Exception as e:
            st.info("Using enhanced contour detection for hand-drawn sketches...")
        
        # Use enhanced fallback detection for hand-drawn sketches
        return self.fallback_detection(image)
    
    def fallback_detection(self, image):
        """
        Enhanced fallback detection using OpenCV contour detection for hand-drawn sketches.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            List of detected elements
        """
        try:
            # Convert PIL to numpy if needed
            if isinstance(image, Image.Image):
                img_array = np.array(image)
            else:
                img_array = image
            
            # Convert to grayscale
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Enhanced preprocessing for hand-drawn sketches
            processed = self._preprocess_for_handdrawn(gray)
            
            # Find contours
            contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            detected_elements = []
            
            for contour in contours:
                # Filter small contours
                area = cv2.contourArea(contour)
                if area < 50:  # Lower threshold for hand-drawn elements
                    continue
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter very small elements
                if w < 10 or h < 10:
                    continue
                
                # Determine element type based on shape and context
                element_type = self.classify_handdrawn_shape(contour, w, h, gray)
                
                # Calculate confidence based on shape regularity
                confidence = self.calculate_confidence(contour, w, h)
                
                detected_elements.append({
                    'type': element_type,
                    'bbox': [x, y, x + w, y + h],
                    'confidence': confidence,
                    'center': [x + w // 2, y + h // 2]
                })
            
            # Sort by confidence
            detected_elements.sort(key=lambda x: x['confidence'], reverse=True)
            
            return detected_elements
            
        except Exception as e:
            st.error(f"Fallback detection failed: {str(e)}")
            return []
    
    def _preprocess_for_handdrawn(self, gray):
        """
        Preprocesses image specifically for hand-drawn sketch detection.
        
        Args:
            gray: Grayscale image
            
        Returns:
            Preprocessed binary image
        """
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Apply adaptive thresholding for better edge detection
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Apply morphological operations to connect broken lines
        kernel = np.ones((2, 2), np.uint8)
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Remove small noise
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
        
        return cleaned
    
    def classify_handdrawn_shape(self, contour, width, height, original_gray):
        """
        Enhanced shape classification for hand-drawn UI elements.
        
        Args:
            contour: OpenCV contour
            width: Width of bounding rectangle
            height: Height of bounding rectangle
            original_gray: Original grayscale image for context
            
        Returns:
            String representing the UI element type
        """
        # Calculate aspect ratio
        aspect_ratio = width / height if height > 0 else 0
        
        # Calculate contour area and bounding rectangle area
        contour_area = cv2.contourArea(contour)
        rect_area = width * height
        extent = contour_area / rect_area if rect_area > 0 else 0
        
        # Get contour properties
        perimeter = cv2.arcLength(contour, True)
        circularity = 4 * np.pi * contour_area / (perimeter * perimeter) if perimeter > 0 else 0
        
        # Analyze the region for text content
        x, y, w, h = cv2.boundingRect(contour)
        region = original_gray[y:y+h, x:x+w]
        
        # Check if region contains text-like patterns
        has_text_patterns = self._has_text_patterns(region)
        
        # Enhanced classification logic for hand-drawn elements
        if has_text_patterns:
            if aspect_ratio > 2:  # Wide text
                return 'input'
            elif aspect_ratio < 0.5:  # Tall text
                return 'textarea'
            else:
                return 'text'
        elif aspect_ratio > 4:  # Very wide rectangle
            return 'input'
        elif aspect_ratio < 0.3:  # Very tall rectangle
            return 'textarea'
        elif 0.8 < aspect_ratio < 1.5 and extent > 0.6:  # Square-ish and mostly filled
            return 'button'
        elif circularity > 0.7:  # Circular or rounded
            return 'button'
        elif extent < 0.4:  # Low fill ratio (likely outline)
            if aspect_ratio > 2:
                return 'input'
            else:
                return 'text'
        elif width > 100 and height > 30:  # Large rectangular area
            return 'card'
        else:
            return 'element'
    
    def _has_text_patterns(self, region):
        """
        Checks if a region contains text-like patterns.
        
        Args:
            region: Image region to analyze
            
        Returns:
            Boolean indicating if region contains text patterns
        """
        if region.size == 0:
            return False
        
        # Apply edge detection
        edges = cv2.Canny(region, 50, 150)
        
        # Count edge pixels
        edge_pixels = np.sum(edges > 0)
        total_pixels = region.size
        
        # Calculate edge density
        edge_density = edge_pixels / total_pixels if total_pixels > 0 else 0
        
        # Text regions typically have higher edge density
        return edge_density > 0.1
    
    def calculate_confidence(self, contour, width, height):
        """
        Calculates confidence score for detected element.
        
        Args:
            contour: OpenCV contour
            width: Width of bounding rectangle
            height: Height of bounding rectangle
            
        Returns:
            Confidence score between 0 and 1
        """
        # Calculate contour area and bounding rectangle area
        contour_area = cv2.contourArea(contour)
        rect_area = width * height
        extent = contour_area / rect_area if rect_area > 0 else 0
        
        # Calculate perimeter and circularity
        perimeter = cv2.arcLength(contour, True)
        circularity = 4 * np.pi * contour_area / (perimeter * perimeter) if perimeter > 0 else 0
        
        # Base confidence on shape regularity
        shape_confidence = min(extent, 1.0)
        
        # Boost confidence for well-defined shapes
        if circularity > 0.7:  # Circular shapes
            shape_confidence *= 1.2
        elif extent > 0.8:  # Well-filled shapes
            shape_confidence *= 1.1
        
        # Size-based confidence (larger elements are more likely to be intentional)
        size_confidence = min((width * height) / 1000, 1.0)
        
        # Combine confidences
        final_confidence = (shape_confidence + size_confidence) / 2
        
        return min(final_confidence, 1.0)
    
    def visualize_detections(self, image, detections):
        """
        Visualizes detected elements on the image.
        
        Args:
            image: PIL Image or numpy array
            detections: List of detected elements
            
        Returns:
            Image with bounding boxes drawn
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
        
        # Draw bounding boxes
        for detection in detections:
            bbox = detection['bbox']
            element_type = detection['type']
            confidence = detection['confidence']
            
            # Draw rectangle
            cv2.rectangle(img_bgr, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            
            # Add label
            label = f"{element_type}: {confidence:.2f}"
            cv2.putText(img_bgr, label, (bbox[0], bbox[1] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Convert back to RGB for display
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        return Image.fromarray(img_rgb)
    
    def save_detections(self, detections, filename="detections.json"):
        """
        Saves detection results to a JSON file.
        
        Args:
            detections: List of detected elements
            filename: Name of the output file
        """
        os.makedirs("temp", exist_ok=True)
        file_path = os.path.join("temp", filename)
        
        with open(file_path, 'w') as f:
            json.dump(detections, f, indent=2)
        
        return file_path

# Example usage
if __name__ == "__main__":
    detector = UIElementDetector()
    
    # Test with a sample image
    test_image = np.zeros((400, 600, 3), dtype=np.uint8)
    test_image.fill(255)  # White background
    
    # Draw some test shapes
    cv2.rectangle(test_image, (50, 50), (150, 100), (0, 0, 0), 2)  # Button
    cv2.rectangle(test_image, (200, 50), (400, 80), (0, 0, 0), 2)  # Input
    
    detections = detector.detect_elements(test_image)
    print(f"Detected {len(detections)} elements:")
    for detection in detections:
        print(f"- {detection['type']}: {detection['bbox']} (conf: {detection['confidence']:.2f})") 