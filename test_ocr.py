#!/usr/bin/env python3
"""
Test script for improved OCR functionality.
This script tests the enhanced text extraction capabilities.
"""

import cv2
import numpy as np
from PIL import Image
import os
from ocr import TextExtractor

def create_test_image():
    """Create a test image with handwritten-like text."""
    # Create a white background
    img = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Add some "handwritten" text using different fonts and styles
    texts = [
        ("Submit", (50, 50), 1.2, 2),
        ("Username", (50, 100), 1.0, 2),
        ("Password", (50, 150), 1.0, 2),
        ("Login", (50, 200), 1.2, 2),
        ("Sign Up", (50, 250), 1.0, 2),
        ("Search", (300, 50), 1.0, 2),
        ("Cancel", (300, 100), 1.0, 2),
        ("Save", (300, 150), 1.0, 2),
        ("Delete", (300, 200), 1.0, 2),
        ("Edit", (300, 250), 1.0, 2)
    ]
    
    for text, pos, scale, thickness in texts:
        # Add some noise to make it look more handwritten
        cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), thickness)
        
        # Add slight random offset to simulate handwriting
        offset_x = np.random.randint(-3, 4)
        offset_y = np.random.randint(-3, 4)
        cv2.putText(img, text, (pos[0] + offset_x, pos[1] + offset_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, scale * 0.8, (0, 0, 0), 1)
    
    return Image.fromarray(img)

def test_ocr_functionality():
    """Test the OCR functionality with different scenarios."""
    print("🧪 Testing Enhanced OCR Functionality...")
    
    # Initialize the text extractor
    extractor = TextExtractor()
    
    # Create test image
    print("📝 Creating test image...")
    test_image = create_test_image()
    
    # Test 1: Extract text from entire image
    print("\n🔍 Test 1: Extracting text from entire image...")
    text_regions = extractor.extract_text_from_image(test_image)
    
    print(f"Found {len(text_regions)} text regions:")
    for i, region in enumerate(text_regions):
        print(f"  {i+1}. '{region['text']}' (confidence: {region['confidence']:.2f})")
    
    # Test 2: Test specific regions
    print("\n🎯 Test 2: Testing specific regions...")
    test_regions = [
        [40, 40, 150, 80],   # Submit area
        [40, 90, 150, 130],  # Username area
        [290, 40, 400, 80],  # Search area
    ]
    
    for i, bbox in enumerate(test_regions):
        text = extractor.extract_text_from_region(test_image, bbox)
        print(f"  Region {i+1} {bbox}: '{text}'")
    
    # Test 3: Test preprocessing techniques
    print("\n🛠️ Test 3: Testing preprocessing techniques...")
    processed_images = extractor.preprocess_for_ocr(test_image)
    print(f"  Generated {len(processed_images)} different preprocessing techniques")
    
    # Test 4: Test text cleaning
    print("\n🧹 Test 4: Testing text cleaning...")
    test_texts = [
        "submit",
        "usernam3",  # Common OCR mistake
        "passw0rd",  # Common OCR mistake
        "l0gin",     # Common OCR mistake
        "s3arch"     # Common OCR mistake
    ]
    
    for text in test_texts:
        cleaned = extractor.clean_text(text)
        print(f"  '{text}' -> '{cleaned}'")
    
    print("\n✅ OCR testing completed!")
    return text_regions

def save_test_results(text_regions):
    """Save test results to a file."""
    os.makedirs("temp", exist_ok=True)
    
    # Save as JSON
    import json
    with open("temp/ocr_test_results.json", "w") as f:
        json.dump(text_regions, f, indent=2)
    
    print("💾 Test results saved to temp/ocr_test_results.json")

if __name__ == "__main__":
    try:
        # Run the tests
        results = test_ocr_functionality()
        
        # Save results
        save_test_results(results)
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc() 