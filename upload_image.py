import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import os

class ImageUploader:
    """Handles image upload and preprocessing for UI sketch analysis."""
    
    def __init__(self):
        self.supported_formats = ['png', 'jpg', 'jpeg', 'bmp', 'tiff']
        self.max_file_size = 10 * 1024 * 1024  # 10MB
    
    def upload_image(self):
        """
        Creates a Streamlit file uploader for UI sketches.
        Returns the uploaded image as a PIL Image object.
        """
        st.subheader("📱 Upload Your UI Sketch")
        st.write("Upload a hand-drawn UI sketch to convert it into working React code.")
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=self.supported_formats,
            help="Supported formats: PNG, JPG, JPEG, BMP, TIFF (max 10MB)"
        )
        
        if uploaded_file is not None:
            # Check file size
            if uploaded_file.size > self.max_file_size:
                st.error(f"File size too large. Maximum size is {self.max_file_size // (1024*1024)}MB")
                return None
            
            try:
                # Convert to PIL Image
                image = Image.open(uploaded_file)
                
                # Display the uploaded image
                st.image(image, caption="Uploaded UI Sketch", use_column_width=True)
                
                return image
                
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                return None
        
        return None
    
    def preprocess_image(self, image):
        """
        Preprocesses the image for better object detection and OCR.
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed image as numpy array
        """
        # Convert PIL to OpenCV format
        img_array = np.array(image)
        
        # Convert RGB to BGR if needed
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Apply preprocessing steps for better detection
        # 1. Convert to grayscale for better contrast
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        
        # 2. Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 3. Apply adaptive thresholding for better edge detection
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # 4. Apply morphological operations to clean up the image
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def save_uploaded_image(self, image, filename="uploaded_sketch.png"):
        """
        Saves the uploaded image to a temporary file.
        
        Args:
            image: PIL Image object
            filename: Name of the file to save
            
        Returns:
            Path to the saved file
        """
        # Create temp directory if it doesn't exist
        os.makedirs("temp", exist_ok=True)
        
        file_path = os.path.join("temp", filename)
        image.save(file_path)
        
        return file_path
    
    def cleanup_temp_files(self):
        """Removes temporary files created during processing."""
        import shutil
        if os.path.exists("temp"):
            shutil.rmtree("temp")

# Example usage
if __name__ == "__main__":
    uploader = ImageUploader()
    image = uploader.upload_image()
    
    if image:
        processed_image = uploader.preprocess_image(image)
        st.image(processed_image, caption="Preprocessed Image", use_column_width=True) 