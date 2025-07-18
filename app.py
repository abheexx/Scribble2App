import streamlit as st
import os
import json
from PIL import Image
import tempfile
import shutil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our custom modules
from upload_image import ImageUploader
from detect_elements import UIElementDetector
from ocr import TextExtractor
from schema_builder import UISchemaBuilder
from code_gen import ReactCodeGenerator

# Page configuration
st.set_page_config(
    page_title="Scribble2App - Convert Sketches to React Code",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .step-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class Scribble2App:
    """Main application class that orchestrates the entire pipeline."""
    
    def __init__(self):
        self.uploader = ImageUploader()
        self.detector = UIElementDetector()
        self.extractor = TextExtractor()
        self.builder = UISchemaBuilder()
        self.generator = ReactCodeGenerator()
        
        # Initialize session state
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 0
        if 'uploaded_image' not in st.session_state:
            st.session_state.uploaded_image = None
        if 'detected_elements' not in st.session_state:
            st.session_state.detected_elements = []
        if 'text_regions' not in st.session_state:
            st.session_state.text_regions = []
        if 'ui_schema' not in st.session_state:
            st.session_state.ui_schema = {}
        if 'generated_code' not in st.session_state:
            st.session_state.generated_code = {}
    
    def run(self):
        """Main application loop."""
        # Header
        st.markdown('<h1 class="main-header">🎨 Scribble2App</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Convert your hand-drawn UI sketches into working React code with AI</p>', unsafe_allow_html=True)
        
        # Sidebar for navigation and settings
        self.render_sidebar()
        
        # Main content area
        if st.session_state.current_step == 0:
            self.step_upload_image()
        elif st.session_state.current_step == 1:
            self.step_detect_elements()
        elif st.session_state.current_step == 2:
            self.step_extract_text()
        elif st.session_state.current_step == 3:
            self.step_build_schema()
        elif st.session_state.current_step == 4:
            self.step_generate_code()
        elif st.session_state.current_step == 5:
            self.step_download_results()
    
    def render_sidebar(self):
        """Renders the sidebar with navigation and settings."""
        with st.sidebar:
            st.markdown("## 📋 Pipeline Steps")
            
            steps = [
                "📤 Upload Image",
                "🔍 Detect Elements", 
                "📝 Extract Text",
                "🏗️ Build Schema",
                "⚡ Generate Code",
                "📥 Download Results"
            ]
            
            for i, step in enumerate(steps):
                if i == st.session_state.current_step:
                    st.markdown(f"**{step}** ✅")
                elif i < st.session_state.current_step:
                    st.markdown(f"~~{step}~~ ✅")
                else:
                    st.markdown(f"{step} ⏳")
            
            st.markdown("---")
            
            # Settings
            st.markdown("## ⚙️ Settings")
            
            # Confidence threshold
            confidence_threshold = st.slider(
                "Detection Confidence",
                min_value=0.1,
                max_value=0.9,
                value=0.5,
                step=0.1,
                help="Minimum confidence for element detection"
            )
            
            # Code generation settings
            use_typescript = st.checkbox("Use TypeScript", value=True)
            include_tests = st.checkbox("Include Tests", value=False)
            
            st.markdown("---")
            
            # Reset button
            if st.button("🔄 Reset Pipeline"):
                self.reset_pipeline()
            
            # Help section
            st.markdown("## ❓ Help")
            st.markdown("""
            **How to use:**
            1. Upload a hand-drawn UI sketch
            2. Let AI detect UI elements
            3. Extract handwritten text
            4. Generate React code
            5. Download your project
            
            **Supported formats:** PNG, JPG, JPEG, BMP, TIFF
            **Max file size:** 10MB
            """)
    
    def step_upload_image(self):
        """Step 1: Upload and preprocess image."""
        st.markdown('<h2 class="sub-header">📤 Step 1: Upload Your UI Sketch</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Upload image
            uploaded_image = self.uploader.upload_image()
            
            if uploaded_image:
                st.session_state.uploaded_image = uploaded_image
                # Show image info
                with col2:
                    st.markdown("### 📊 Image Info")
                    st.write(f"**Size:** {uploaded_image.size[0]} × {uploaded_image.size[1]} pixels")
                    st.write(f"**Mode:** {uploaded_image.mode}")
                    st.write(f"**Format:** {uploaded_image.format}")
                # Preprocess image
                with st.spinner("🔄 Preprocessing image..."):
                    processed_image = self.uploader.preprocess_image(uploaded_image)
                # Show processed image
                st.markdown("### 🔧 Preprocessed Image")
                st.image(processed_image, caption="Preprocessed for better detection", use_column_width=True)
                # Next step button
                if st.button("➡️ Continue to Element Detection", type="primary"):
                    st.session_state.current_step = 1
                    st.rerun()
            else:
                # Show example
                with col2:
                    st.markdown("### 💡 Example")
                    st.markdown("""
                    **Draw a simple UI sketch like:**
                    - Buttons
                    - Input fields
                    - Text labels
                    - Images
                    - Forms
                    """)
    
    def step_detect_elements(self):
        """Step 2: Detect UI elements in the image."""
        st.markdown('<h2 class="sub-header">🔍 Step 2: Detect UI Elements</h2>', unsafe_allow_html=True)
        
        if st.session_state.uploaded_image is None:
            st.error("❌ No image uploaded. Please go back to step 1.")
            if st.button("⬅️ Back to Upload"):
                st.session_state.current_step = 0
                st.rerun()
            return
        
        # Detect elements
        with st.spinner("🔍 Detecting UI elements..."):
            detected_elements = self.detector.detect_elements(st.session_state.uploaded_image)
            st.session_state.detected_elements = detected_elements
        
        # Show results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📊 Detection Results")
            if detected_elements:
                st.success(f"✅ Detected {len(detected_elements)} UI elements")
                
                # Show detection details
                for i, element in enumerate(detected_elements):
                    with st.expander(f"Element {i+1}: {element['type']} (Confidence: {element['confidence']:.2f})"):
                        st.write(f"**Type:** {element['type']}")
                        st.write(f"**Position:** {element['bbox']}")
                        st.write(f"**Center:** {element['center']}")
                        st.write(f"**Confidence:** {element['confidence']:.2f}")
            else:
                st.warning("⚠️ No elements detected. Try a clearer sketch.")
        
        with col2:
            # Visualize detections
            if detected_elements:
                st.markdown("### 🎯 Visualized Detections")
                visualized_image = self.detector.visualize_detections(
                    st.session_state.uploaded_image, 
                    detected_elements
                )
                st.image(visualized_image, caption="Detected elements highlighted", use_column_width=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⬅️ Back to Upload"):
                st.session_state.current_step = 0
                st.rerun()
        
        with col3:
            if detected_elements and st.button("➡️ Continue to Text Extraction", type="primary"):
                st.session_state.current_step = 2
                st.rerun()
    
    def step_extract_text(self):
        """Step 3: Extract text from the image."""
        st.markdown('<h2 class="sub-header">📝 Step 3: Extract Text</h2>', unsafe_allow_html=True)
        
        if not st.session_state.detected_elements:
            st.error("❌ No elements detected. Please go back to step 2.")
            if st.button("⬅️ Back to Detection"):
                st.session_state.current_step = 1
                st.rerun()
            return
        
        # Extract text with enhanced OCR
        with st.spinner("📝 Extracting text with enhanced OCR..."):
            text_regions = self.extractor.extract_text_from_image(st.session_state.uploaded_image)
            st.session_state.text_regions = text_regions
            
            # Get OCR feedback
            ocr_feedback = self.extractor.get_ocr_feedback(st.session_state.uploaded_image)
        
        # Show results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📊 Text Extraction Results")
            if text_regions:
                st.success(f"✅ Extracted {len(text_regions)} text regions")
                
                # Show OCR feedback
                if 'suggestions' in ocr_feedback:
                    st.markdown("#### 💡 OCR Feedback")
                    for suggestion in ocr_feedback['suggestions']:
                        st.info(suggestion)
                
                # Show confidence breakdown
                if 'high_confidence' in ocr_feedback:
                    st.markdown("#### 📈 Confidence Breakdown")
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("High Confidence", ocr_feedback['high_confidence'])
                    with col_b:
                        st.metric("Medium Confidence", ocr_feedback['medium_confidence'])
                    with col_c:
                        st.metric("Low Confidence", ocr_feedback['low_confidence'])
                
                # Show extracted text
                st.markdown("#### 📝 Detected Text")
                for i, region in enumerate(text_regions):
                    confidence_color = "🟢" if region['confidence'] > 0.7 else "🟡" if region['confidence'] > 0.4 else "🔴"
                    with st.expander(f"{confidence_color} Text {i+1}: '{region['text']}' (Confidence: {region['confidence']:.2f})"):
                        st.write(f"**Text:** '{region['text']}'")
                        st.write(f"**Position:** {region['bbox']}")
                        st.write(f"**Confidence:** {region['confidence']:.2f}")
                        
                        # Add manual correction option
                        corrected_text = st.text_input(f"Correct text {i+1} (optional):", value=region['text'], key=f"correct_{i}")
                        if corrected_text != region['text']:
                            text_regions[i]['text'] = corrected_text
                            st.session_state.text_regions = text_regions
                            st.success("✅ Text corrected!")
            else:
                st.warning("⚠️ No text detected. The sketch might not contain handwritten text.")
                
                # Show suggestions for improvement
                if 'suggestions' in ocr_feedback:
                    st.markdown("#### 💡 Suggestions for Better Text Detection:")
                    for suggestion in ocr_feedback['suggestions']:
                        st.info(suggestion)
        
        with col2:
            # Visualize text regions
            if text_regions:
                st.markdown("### 🎯 Visualized Text Regions")
                visualized_text = self.extractor.visualize_text_regions(
                    st.session_state.uploaded_image,
                    text_regions
                )
                st.image(visualized_text, caption="Text regions highlighted", use_column_width=True)
            else:
                st.markdown("### 🎯 Original Image")
                st.image(st.session_state.uploaded_image, caption="No text regions detected", use_column_width=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⬅️ Back to Detection"):
                st.session_state.current_step = 1
                st.rerun()
        
        with col3:
            if st.button("➡️ Continue to Schema Building", type="primary"):
                st.session_state.current_step = 3
                st.rerun()
    
    def step_build_schema(self):
        """Step 4: Build UI schema from detected elements and text."""
        st.markdown('<h2 class="sub-header">🏗️ Step 4: Build UI Schema</h2>', unsafe_allow_html=True)
        
        if not st.session_state.detected_elements:
            st.error("❌ No elements detected. Please go back to step 2.")
            if st.button("⬅️ Back to Detection"):
                st.session_state.current_step = 1
                st.rerun()
            return
        
        # Build schema
        with st.spinner("🏗️ Building UI schema..."):
            image_size = st.session_state.uploaded_image.size
            ui_schema = self.builder.build_schema(
                st.session_state.detected_elements,
                st.session_state.text_regions,
                image_size
            )
            st.session_state.ui_schema = ui_schema
        
        # Show schema
        st.markdown("### 📊 Generated UI Schema")
        
        if ui_schema:
            st.success("✅ UI schema built successfully!")
            
            # Schema details
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### 📋 Schema Overview")
                st.write(f"**Layout Type:** {ui_schema.get('layout', 'Unknown')}")
                st.write(f"**Total Components:** {len(ui_schema.get('components', []))}")
                st.write(f"**Image Size:** {ui_schema.get('metadata', {}).get('image_size', 'Unknown')}")
                
                # Show components
                st.markdown("#### 🧩 Components")
                for i, component in enumerate(ui_schema.get('components', [])):
                    with st.expander(f"Component {i+1}: {component.get('type', 'Unknown')}"):
                        st.json(component)
            
            with col2:
                # Show full schema
                st.markdown("#### 📄 Full Schema (JSON)")
                st.json(ui_schema)
        else:
            st.error("❌ Failed to build schema.")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⬅️ Back to Text Extraction"):
                st.session_state.current_step = 2
                st.rerun()
        
        with col3:
            if ui_schema and st.button("➡️ Continue to Code Generation", type="primary"):
                st.session_state.current_step = 4
                st.rerun()
    
    def step_generate_code(self):
        """Step 5: Generate React code from UI schema."""
        st.markdown('<h2 class="sub-header">⚡ Step 5: Generate React Code</h2>', unsafe_allow_html=True)
        
        if not st.session_state.ui_schema:
            st.error("❌ No UI schema available. Please go back to step 4.")
            if st.button("⬅️ Back to Schema Building"):
                st.session_state.current_step = 3
                st.rerun()
            return
        
        # Check OpenAI API key
        if not os.getenv('OPENAI_API_KEY'):
            st.error("❌ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
            st.info("You can set it in your terminal: `export OPENAI_API_KEY='your-api-key-here'`")
            return
        
        # Generate code
        with st.spinner("⚡ Generating React code..."):
            generated_code = self.generator.generate_react_code(st.session_state.ui_schema)
            st.session_state.generated_code = generated_code
        
        # Show results
        if generated_code:
            st.success("✅ React code generated successfully!")
            
            # Show generated files
            st.markdown("### 📁 Generated Files")
            
            # Main App component
            if 'app_jsx' in generated_code:
                with st.expander("📄 App.jsx (Main Component)"):
                    st.code(generated_code['app_jsx'], language='jsx')
            
            # Package.json
            if 'package_json' in generated_code:
                with st.expander("📦 package.json"):
                    st.code(generated_code['package_json'], language='json')
            
            # Tailwind config
            if 'tailwind_config' in generated_code:
                with st.expander("🎨 tailwind.config.js"):
                    st.code(generated_code['tailwind_config'], language='javascript')
            
            # Other components
            if 'components' in generated_code and generated_code['components']:
                st.markdown("#### 🧩 Individual Components")
                for component_name, component_code in generated_code['components'].items():
                    with st.expander(f"📄 {component_name}"):
                        st.code(component_code, language='jsx')
            
            # README
            if 'readme_md' in generated_code:
                with st.expander("📖 README.md"):
                    st.markdown(generated_code['readme_md'])
        else:
            st.error("❌ Failed to generate code. Check your OpenAI API key and try again.")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⬅️ Back to Schema Building"):
                st.session_state.current_step = 3
                st.rerun()
        
        with col3:
            if generated_code and st.button("➡️ Continue to Download", type="primary"):
                st.session_state.current_step = 5
                st.rerun()
    
    def step_download_results(self):
        """Step 6: Download the generated React project."""
        st.markdown('<h2 class="sub-header">📥 Step 6: Download Results</h2>', unsafe_allow_html=True)
        
        if not st.session_state.generated_code:
            st.error("❌ No code generated. Please go back to step 5.")
            if st.button("⬅️ Back to Code Generation"):
                st.session_state.current_step = 4
                st.rerun()
            return
        
        # Create project zip
        with st.spinner("📦 Creating project package..."):
            zip_path = self.generator.create_project_zip(st.session_state.generated_code)
        
        if zip_path:
            st.success("✅ Project package created successfully!")
            
            # Download button
            with open(zip_path, 'rb') as f:
                st.download_button(
                    label="📥 Download React Project (ZIP)",
                    data=f.read(),
                    file_name="scribble2app-react-project.zip",
                    mime="application/zip",
                    type="primary"
                )
            
            # Project info
            st.markdown("### 📋 Project Information")
            st.markdown("""
            **What you'll get:**
            - Complete React application
            - Tailwind CSS styling
            - Vite build configuration
            - TypeScript support
            - ESLint configuration
            - README with setup instructions
            
            **To run the project:**
            1. Extract the ZIP file
            2. Run `npm install`
            3. Run `npm run dev`
            4. Open `http://localhost:5173`
            """)
            
            # Show preview
            st.markdown("### 👀 Code Preview")
            if 'app_jsx' in st.session_state.generated_code:
                st.code(st.session_state.generated_code['app_jsx'], language='jsx')
        else:
            st.error("❌ Failed to create project package.")
        
        # Navigation and restart
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⬅️ Back to Code Generation"):
                st.session_state.current_step = 4
                st.rerun()
        
        with col2:
            if st.button("🔄 Start New Project"):
                self.reset_pipeline()
                st.rerun()
        
        with col3:
            if st.button("📊 View All Results"):
                self.show_all_results()
    
    def show_all_results(self):
        """Shows all results in a comprehensive view."""
        st.markdown('<h2 class="sub-header">📊 All Results</h2>', unsafe_allow_html=True)
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🖼️ Original Image", 
            "🔍 Detections", 
            "📝 Text", 
            "🏗️ Schema", 
            "⚡ Code"
        ])
        
        with tab1:
            if st.session_state.uploaded_image:
                st.image(st.session_state.uploaded_image, caption="Original Sketch", use_column_width=True)
        
        with tab2:
            if st.session_state.detected_elements:
                st.json(st.session_state.detected_elements)
        
        with tab3:
            if st.session_state.text_regions:
                st.json(st.session_state.text_regions)
        
        with tab4:
            if st.session_state.ui_schema:
                st.json(st.session_state.ui_schema)
        
        with tab5:
            if st.session_state.generated_code:
                for file_name, file_content in st.session_state.generated_code.items():
                    with st.expander(f"📄 {file_name}"):
                        if file_name.endswith('.md'):
                            st.markdown(file_content)
                        elif file_name.endswith('.json'):
                            st.code(file_content, language='json')
                        else:
                            st.code(file_content, language='jsx')
    
    def reset_pipeline(self):
        """Resets the entire pipeline."""
        st.session_state.current_step = 0
        st.session_state.uploaded_image = None
        st.session_state.detected_elements = []
        st.session_state.text_regions = []
        st.session_state.ui_schema = {}
        st.session_state.generated_code = {}
        
        # Clean up temp files
        self.uploader.cleanup_temp_files()

def main():
    """Main function to run the Streamlit app."""
    app = Scribble2App()
    app.run()

if __name__ == "__main__":
    main() 