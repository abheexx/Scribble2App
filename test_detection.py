#!/usr/bin/env python3
"""
Test script for improved element detection for hand-drawn sketches.
"""

import cv2
import numpy as np
from PIL import Image
import os
from detect_elements import UIElementDetector

def create_handdrawn_test_image():
    """Create a test image simulating a hand-drawn login form."""
    # Create a white background
    img = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Draw a hand-drawn login form
    # Login title box
    cv2.rectangle(img, (200, 50), (400, 100), (0, 0, 0), 3)
    cv2.putText(img, "Login", (280, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    # Email label and input
    cv2.putText(img, "Email:", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.rectangle(img, (150, 130), (500, 170), (0, 0, 0), 2)
    
    # Password label and input
    cv2.putText(img, "Password:", (50, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.rectangle(img, (150, 200), (500, 240), (0, 0, 0), 2)
    cv2.putText(img, "----", (160, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    # Submit button
    cv2.rectangle(img, (250, 280), (350, 320), (0, 0, 0), 3)
    cv2.putText(img, "Submit", (270, 305), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    return Image.fromarray(img)

def test_detection():
    """Test the element detection functionality."""
    print("🧪 Testing Enhanced Element Detection for Hand-Drawn Sketches...")
    
    # Initialize the detector
    detector = UIElementDetector()
    
    # Create test image
    print("📝 Creating hand-drawn test image...")
    test_image = create_handdrawn_test_image()
    
    # Test detection
    print("\n🔍 Testing element detection...")
    detected_elements = detector.detect_elements(test_image)
    
    print(f"Found {len(detected_elements)} elements:")
    for i, element in enumerate(detected_elements):
        print(f"  {i+1}. {element['type']} (confidence: {element['confidence']:.2f}) at {element['bbox']}")
    
    # Test visualization
    print("\n🎯 Testing visualization...")
    visualized = detector.visualize_detections(test_image, detected_elements)
    
    # Save results
    os.makedirs("temp", exist_ok=True)
    visualized.save("temp/detection_test_result.png")
    print("💾 Visualization saved to temp/detection_test_result.png")
    
    # Save detection results
    import json
    with open("temp/detection_test_results.json", "w") as f:
        json.dump(detected_elements, f, indent=2)
    print("💾 Detection results saved to temp/detection_test_results.json")
    
    print("\n✅ Detection testing completed!")
    return detected_elements

if __name__ == "__main__":
    try:
        # Run the tests
        results = test_detection()
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc() 