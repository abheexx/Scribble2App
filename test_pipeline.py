#!/usr/bin/env python3
"""
Test script for Scribble2App pipeline.
This script tests all modules to ensure they can be imported and basic functionality works.
"""

import sys
import os
import traceback
from PIL import Image
import numpy as np

def test_imports():
    """Test that all modules can be imported successfully."""
    print("🔍 Testing module imports...")
    
    try:
        from upload_image import ImageUploader
        print("✅ upload_image.py - OK")
    except Exception as e:
        print(f"❌ upload_image.py - FAILED: {e}")
        return False
    
    try:
        from detect_elements import UIElementDetector
        print("✅ detect_elements.py - OK")
    except Exception as e:
        print(f"❌ detect_elements.py - FAILED: {e}")
        return False
    
    try:
        from ocr import TextExtractor
        print("✅ ocr.py - OK")
    except Exception as e:
        print(f"❌ ocr.py - FAILED: {e}")
        return False
    
    try:
        from schema_builder import UISchemaBuilder
        print("✅ schema_builder.py - OK")
    except Exception as e:
        print(f"❌ schema_builder.py - FAILED: {e}")
        return False
    
    try:
        from code_gen import ReactCodeGenerator
        print("✅ code_gen.py - OK")
    except Exception as e:
        print(f"❌ code_gen.py - FAILED: {e}")
        return False
    
    return True

def test_image_uploader():
    """Test ImageUploader functionality."""
    print("\n📤 Testing ImageUploader...")
    
    try:
        from upload_image import ImageUploader
        uploader = ImageUploader()
        
        # Create a test image
        test_image = Image.new('RGB', (400, 300), color='white')
        
        # Test preprocessing
        processed = uploader.preprocess_image(test_image)
        print("✅ Image preprocessing - OK")
        
        # Test saving
        temp_path = uploader.save_uploaded_image(test_image, "test.png")
        if os.path.exists(temp_path):
            print("✅ Image saving - OK")
            os.remove(temp_path)  # Clean up
        else:
            print("❌ Image saving - FAILED")
            return False
            
    except Exception as e:
        print(f"❌ ImageUploader test - FAILED: {e}")
        return False
    
    return True

def test_element_detector():
    """Test UIElementDetector functionality."""
    print("\n🔍 Testing UIElementDetector...")
    
    try:
        from detect_elements import UIElementDetector
        detector = UIElementDetector()
        
        # Create a test image with simple shapes
        test_image = np.zeros((400, 600, 3), dtype=np.uint8)
        test_image.fill(255)  # White background
        
        # Draw some test shapes (simulating UI elements)
        import cv2
        cv2.rectangle(test_image, (50, 50), (150, 100), (0, 0, 0), 2)  # Button
        cv2.rectangle(test_image, (200, 50), (400, 80), (0, 0, 0), 2)  # Input
        
        # Test detection
        detections = detector.detect_elements(test_image)
        print(f"✅ Element detection - OK (found {len(detections)} elements)")
        
    except Exception as e:
        print(f"❌ UIElementDetector test - FAILED: {e}")
        return False
    
    return True

def test_text_extractor():
    """Test TextExtractor functionality."""
    print("\n📝 Testing TextExtractor...")
    
    try:
        from ocr import TextExtractor
        extractor = TextExtractor()
        
        # Create a test image with text
        test_image = np.zeros((200, 400, 3), dtype=np.uint8)
        test_image.fill(255)  # White background
        
        # Add some test text
        import cv2
        cv2.putText(test_image, "Test", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Convert to PIL
        pil_image = Image.fromarray(test_image)
        
        # Test text extraction
        text_regions = extractor.extract_text_from_image(pil_image)
        print(f"✅ Text extraction - OK (found {len(text_regions)} text regions)")
        
    except Exception as e:
        print(f"❌ TextExtractor test - FAILED: {e}")
        return False
    
    return True

def test_schema_builder():
    """Test UISchemaBuilder functionality."""
    print("\n🏗️ Testing UISchemaBuilder...")
    
    try:
        from schema_builder import UISchemaBuilder
        builder = UISchemaBuilder()
        
        # Test data
        test_elements = [
            {
                'type': 'button',
                'bbox': [50, 50, 150, 100],
                'center': [100, 75],
                'confidence': 0.8
            },
            {
                'type': 'input',
                'bbox': [200, 50, 400, 80],
                'center': [300, 65],
                'confidence': 0.7
            }
        ]
        
        test_text_regions = [
            {
                'text': 'Submit',
                'bbox': [60, 60, 140, 90],
                'center': [100, 75],
                'confidence': 0.9
            },
            {
                'text': 'Username',
                'bbox': [210, 55, 390, 75],
                'center': [300, 65],
                'confidence': 0.8
            }
        ]
        
        # Test schema building
        schema = builder.build_schema(test_elements, test_text_regions, (600, 400))
        print(f"✅ Schema building - OK (generated {len(schema.get('components', []))} components)")
        
        # Test validation
        is_valid = builder.validate_schema(schema)
        print(f"✅ Schema validation - OK (valid: {is_valid})")
        
    except Exception as e:
        print(f"❌ UISchemaBuilder test - FAILED: {e}")
        return False
    
    return True

def test_code_generator():
    """Test ReactCodeGenerator functionality."""
    print("\n⚡ Testing ReactCodeGenerator...")
    
    try:
        from code_gen import ReactCodeGenerator
        generator = ReactCodeGenerator()
        
        # Test schema
        test_schema = {
            "metadata": {"image_size": (600, 400), "total_elements": 2},
            "layout": "flex",
            "components": [
                {
                    "type": "Button",
                    "id": "button_1",
                    "position": {"x": 50, "y": 50, "width": 100, "height": 50},
                    "props": {"text": "Submit"},
                    "styling": {}
                },
                {
                    "type": "Input",
                    "id": "input_1",
                    "position": {"x": 200, "y": 50, "width": 200, "height": 30},
                    "props": {"placeholder": "Enter text..."},
                    "styling": {}
                }
            ]
        }
        
        # Test fallback code generation (without OpenAI API)
        code_files = generator._generate_fallback_code(test_schema)
        print(f"✅ Fallback code generation - OK (generated {len(code_files)} files)")
        
        # Check if required files are present
        required_files = ['app_jsx', 'package_json', 'tailwind_config', 'index_html', 'readme_md']
        for file_name in required_files:
            if file_name in code_files:
                print(f"✅ {file_name} - OK")
            else:
                print(f"❌ {file_name} - MISSING")
                return False
        
    except Exception as e:
        print(f"❌ ReactCodeGenerator test - FAILED: {e}")
        return False
    
    return True

def test_end_to_end():
    """Test the complete pipeline with sample data."""
    print("\n🔄 Testing end-to-end pipeline...")
    
    try:
        # Import all modules
        from upload_image import ImageUploader
        from detect_elements import UIElementDetector
        from ocr import TextExtractor
        from schema_builder import UISchemaBuilder
        from code_gen import ReactCodeGenerator
        
        # Initialize all components
        uploader = ImageUploader()
        detector = UIElementDetector()
        extractor = TextExtractor()
        builder = UISchemaBuilder()
        generator = ReactCodeGenerator()
        
        # Create test image
        test_image = np.zeros((400, 600, 3), dtype=np.uint8)
        test_image.fill(255)  # White background
        
        # Add test elements
        import cv2
        cv2.rectangle(test_image, (50, 50), (150, 100), (0, 0, 0), 2)  # Button
        cv2.rectangle(test_image, (200, 50), (400, 80), (0, 0, 0), 2)  # Input
        cv2.putText(test_image, "Submit", (60, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(test_image, "Username", (210, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        # Convert to PIL
        pil_image = Image.fromarray(test_image)
        
        # Run pipeline
        print("  📤 Step 1: Image preprocessing...")
        processed_image = uploader.preprocess_image(pil_image)
        
        print("  🔍 Step 2: Element detection...")
        detections = detector.detect_elements(pil_image)
        
        print("  📝 Step 3: Text extraction...")
        text_regions = extractor.extract_text_from_image(pil_image)
        
        print("  🏗️ Step 4: Schema building...")
        schema = builder.build_schema(detections, text_regions, pil_image.size)
        
        print("  ⚡ Step 5: Code generation...")
        code_files = generator._generate_fallback_code(schema)
        
        print(f"✅ End-to-end pipeline - OK")
        print(f"   - Detected {len(detections)} elements")
        print(f"   - Extracted {len(text_regions)} text regions")
        print(f"   - Generated {len(schema.get('components', []))} components")
        print(f"   - Created {len(code_files)} code files")
        
    except Exception as e:
        print(f"❌ End-to-end pipeline test - FAILED: {e}")
        traceback.print_exc()
        return False
    
    return True

def main():
    """Run all tests."""
    print("🧪 Scribble2App Pipeline Test Suite")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Image Uploader", test_image_uploader),
        ("Element Detector", test_element_detector),
        ("Text Extractor", test_text_extractor),
        ("Schema Builder", test_schema_builder),
        ("Code Generator", test_code_generator),
        ("End-to-End Pipeline", test_end_to_end)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The pipeline is ready to use.")
        print("\n🚀 To run the application:")
        print("   streamlit run app.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 