# 🎨 Scribble2App

> **Transform your hand-drawn UI sketches into working React code with AI-powered magic!**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.0+-38B2AC.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<div align="center">
  <img src="https://img.shields.io/badge/AI-Powered-orange?style=for-the-badge&logo=openai" alt="AI Powered">
  <img src="https://img.shields.io/badge/Computer%20Vision-YOLOv8-red?style=for-the-badge&logo=opencv" alt="Computer Vision">
  <img src="https://img.shields.io/badge/OCR-Tesseract-green?style=for-the-badge&logo=google" alt="OCR">
</div>

## ✨ Features

- 🖼️ **Upload hand-drawn UI sketches** (PNG, JPG, JPEG, BMP, TIFF)
- 🔍 **AI-powered element detection** using YOLOv8 and enhanced contour detection
- 📝 **Handwritten text extraction** with multiple OCR techniques
- 🏗️ **Intelligent UI schema building** from detected elements
- ⚡ **React + Tailwind CSS code generation** using OpenAI GPT-4
- 🎯 **Real-time feedback** and manual correction options
- 📱 **Responsive design** generation
- 🚀 **One-click deployment** ready code

## 🎯 What You Get

Transform this:
```
┌─────────────────┐
│     Login       │
├─────────────────┤
│ Email: [______] │
│ Pass:  [______] │
├─────────────────┤
│    Submit       │
└─────────────────┘
```

Into this:
```jsx
function LoginForm() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold text-center mb-6">Login</h1>
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input type="email" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <input type="password" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm" />
          </div>
          <button type="submit" className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700">
            Submit
          </button>
        </form>
      </div>
    </div>
  );
}
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+ (for running generated React apps)
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Scribble2App.git
   cd Scribble2App
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   ```bash
   # Option 1: Environment variable
   export OPENAI_API_KEY="your-api-key-here"
   
   # Option 2: Create .env file
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📖 How to Use

### Step 1: Upload Your Sketch
- Draw a UI sketch on paper or use a drawing app
- Upload the image (PNG, JPG, JPEG, BMP, TIFF)
- Supported file size: up to 10MB

### Step 2: Detect Elements
- AI automatically detects UI elements (buttons, inputs, text, etc.)
- Review detected elements with confidence scores
- Manual adjustments available if needed

### Step 3: Extract Text
- OCR extracts handwritten text from your sketch
- Review and correct extracted text
- Get feedback on detection quality

### Step 4: Build Schema
- AI builds a structured UI schema
- Review component hierarchy and layout
- Schema includes positioning and relationships

### Step 5: Generate Code
- GPT-4 generates React + Tailwind CSS code
- Includes proper component structure
- Responsive design and accessibility features

### Step 6: Download & Run
- Download the complete React project
- Install dependencies: `npm install`
- Run locally: `npm start`

## 🛠️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Upload Image  │───▶│ Detect Elements │───▶│ Extract Text    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Download App  │◀───│ Generate Code   │◀───│ Build Schema    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components

- **`upload_image.py`**: Image preprocessing and validation
- **`detect_elements.py`**: YOLOv8 + enhanced contour detection
- **`ocr.py`**: Multi-technique OCR for handwritten text
- **`schema_builder.py`**: UI schema generation
- **`code_gen.py`**: GPT-4 powered React code generation
- **`app.py`**: Streamlit web interface

## 🎨 Supported UI Elements

| Element | Detection | Generated Component |
|---------|-----------|-------------------|
| Button | ✅ | `<button>` with Tailwind styling |
| Input Field | ✅ | `<input>` with proper types |
| Text Label | ✅ | `<label>` with semantic HTML |
| Text Area | ✅ | `<textarea>` component |
| Card | ✅ | `<div>` with shadow and border |
| Header | ✅ | `<header>` with navigation |
| Image | ✅ | `<img>` with responsive sizing |
| Form | ✅ | `<form>` with validation |

## 🔧 Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your-openai-api-key

# Optional
MODEL_NAME=gpt-4
MAX_TOKENS=2000
DETECTION_CONFIDENCE=0.5
```

### Customization

- **Detection Confidence**: Adjust in the sidebar (0.1 - 0.9)
- **Code Generation**: Toggle TypeScript and test generation
- **OCR Techniques**: Multiple preprocessing methods automatically applied

## 📊 Performance

- **Element Detection**: ~100ms per image
- **Text Extraction**: ~200ms per image  
- **Code Generation**: ~5-10 seconds
- **Total Pipeline**: ~10-15 seconds

## 🚀 Deployment

### Local Development
```bash
npm install
npm start
```

### Production Deployment
```bash
npm run build
# Deploy to Vercel, Netlify, or any hosting platform
```

### Docker Deployment
```bash
docker build -t scribble2app .
docker run -p 8501:8501 scribble2app
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Development Setup
```bash
git clone https://github.com/yourusername/Scribble2App.git
cd Scribble2App
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

### Running Tests
```bash
python -m pytest tests/
python test_pipeline.py
python test_ocr.py
python test_detection.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [YOLOv8](https://github.com/ultralytics/ultralytics) for object detection
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for text extraction
- [OpenAI GPT-4](https://openai.com) for code generation
- [Streamlit](https://streamlit.io) for the web interface
- [Tailwind CSS](https://tailwindcss.com) for styling

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/Scribble2App/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/Scribble2App/discussions)
- 📧 **Email**: your-email@example.com

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/Scribble2App&type=Date)](https://star-history.com/#yourusername/Scribble2App&Date)

---

<div align="center">
  <p>Made with ❤️ by <a href="https://github.com/yourusername">Your Name</a></p>
  <p>If this project helps you, please give it a ⭐ on GitHub!</p>
</div> 