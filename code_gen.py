import openai
import json
import streamlit as st
import os
from typing import Dict, Any, List
import zipfile
from datetime import datetime

class ReactCodeGenerator:
    """Uses OpenAI GPT-4 to generate React + Tailwind CSS code from UI schema."""
    
    def __init__(self):
        self.client = None
        self.setup_openai()
    
    def setup_openai(self):
        """Sets up OpenAI client with API key."""
        try:
            # Get API key from environment variable
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                st.error("❌ OPENAI_API_KEY environment variable not found")
                st.info("Please set your OpenAI API key in the environment variables")
                return
            
            self.client = openai.OpenAI(api_key=api_key)
            st.success("✅ OpenAI client initialized successfully")
            
        except Exception as e:
            st.error(f"❌ Error setting up OpenAI: {str(e)}")
    
    def generate_react_code(self, schema: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates React + Tailwind CSS code from UI schema using GPT-4.
        
        Args:
            schema: UI schema dictionary
            
        Returns:
            Dictionary containing generated code files
        """
        if not self.client:
            st.error("OpenAI client not initialized")
            return {}
        
        try:
            # Create the prompt for code generation
            prompt = self._create_code_generation_prompt(schema)
            
            # Define the function schema for structured output
            functions = [
                {
                    "name": "generate_react_app",
                    "description": "Generate a complete React application with Tailwind CSS",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_jsx": {
                                "type": "string",
                                "description": "Main App.jsx component"
                            },
                            "components": {
                                "type": "object",
                                "description": "Individual React components",
                                "additionalProperties": {
                                    "type": "string"
                                }
                            },
                            "package_json": {
                                "type": "string",
                                "description": "Package.json dependencies"
                            },
                            "tailwind_config": {
                                "type": "string",
                                "description": "Tailwind CSS configuration"
                            },
                            "index_html": {
                                "type": "string",
                                "description": "HTML template"
                            },
                            "readme_md": {
                                "type": "string",
                                "description": "README file with setup instructions"
                            }
                        },
                        "required": ["app_jsx", "components", "package_json", "tailwind_config", "index_html", "readme_md"]
                    }
                }
            ]
            
            # Call GPT-4 with function calling
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert React developer who creates beautiful, modern UI components using React and Tailwind CSS. Generate clean, functional code that follows best practices."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                functions=functions,
                function_call={"name": "generate_react_app"},
                temperature=0.3,
                max_tokens=4000
            )
            
            # Extract the function call response
            function_call = response.choices[0].message.function_call
            if function_call and function_call.name == "generate_react_app":
                arguments = json.loads(function_call.arguments)
                return arguments
            else:
                st.error("Failed to generate structured code response")
                return {}
                
        except Exception as e:
            st.error(f"Error generating React code: {str(e)}")
            return self._generate_fallback_code(schema)
    
    def _create_code_generation_prompt(self, schema: Dict[str, Any]) -> str:
        """
        Creates a detailed prompt for code generation based on the UI schema.
        
        Args:
            schema: UI schema dictionary
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""
Generate a complete React application with Tailwind CSS based on the following UI schema:

SCHEMA:
{json.dumps(schema, indent=2)}

REQUIREMENTS:
1. Create a modern, responsive React application
2. Use Tailwind CSS for styling
3. Implement all components from the schema
4. Use functional components with hooks
5. Include proper TypeScript types
6. Add interactive functionality where appropriate
7. Ensure the layout matches the schema structure
8. Use semantic HTML elements
9. Include proper accessibility attributes
10. Add hover effects and transitions for better UX

COMPONENT MAPPING:
- Button: Interactive button with hover effects
- Input: Form input with proper validation styling
- Text: Display text with appropriate typography
- Textarea: Multi-line text input
- Checkbox: Interactive checkbox with label
- Radio: Radio button group
- Select: Dropdown select component
- Link: Navigation link with hover effects
- Image: Responsive image component
- Card: Container with shadow and padding
- Header: Page header component
- Footer: Page footer component
- Sidebar: Navigation sidebar
- Modal: Overlay modal component
- Table: Data table component

LAYOUT GUIDELINES:
- Use Flexbox and Grid for responsive layouts
- Implement proper spacing using Tailwind's spacing utilities
- Ensure mobile-first responsive design
- Use semantic color schemes
- Add smooth transitions and animations

Please generate the complete application structure with all necessary files.
"""
        return prompt
    
    def _generate_fallback_code(self, schema: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates fallback code when GPT-4 generation fails.
        
        Args:
            schema: UI schema dictionary
            
        Returns:
            Basic fallback code files
        """
        components = schema.get('components', [])
        
        # Generate basic App.jsx
        app_jsx = self._generate_basic_app_jsx(components)
        
        # Generate package.json
        package_json = self._generate_package_json()
        
        # Generate Tailwind config
        tailwind_config = self._generate_tailwind_config()
        
        # Generate HTML template
        index_html = self._generate_index_html()
        
        # Generate README
        readme_md = self._generate_readme()
        
        return {
            "app_jsx": app_jsx,
            "components": {},
            "package_json": package_json,
            "tailwind_config": tailwind_config,
            "index_html": index_html,
            "readme_md": readme_md
        }
    
    def _generate_basic_app_jsx(self, components: List[Dict]) -> str:
        """Generates a basic App.jsx component."""
        component_jsx = ""
        
        for component in components:
            comp_type = component.get('type', 'div')
            comp_id = component.get('id', 'component')
            props = component.get('props', {})
            
            if comp_type == 'Button':
                text = props.get('text', 'Button')
                component_jsx += """
        <button 
          id="{comp_id}"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition-colors duration-200"
          onClick={{() => console.log('{text} clicked')}}
        >
          {text}
        </button>""".format(comp_id=comp_id, text=text)
            
            elif comp_type == 'Input':
                placeholder = props.get('placeholder', 'Enter text...')
                component_jsx += """
        <input 
          id="{comp_id}"
          type="text"
          placeholder="{placeholder}"
          className="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />""".format(comp_id=comp_id, placeholder=placeholder)
            
            elif comp_type == 'Text':
                text = props.get('text', 'Text')
                component_jsx += """
        <p id="{comp_id}" className="text-gray-700 text-base">
          {text}
        </p>""".format(comp_id=comp_id, text=text)
            
            else:
                component_jsx += """
        <div id="{comp_id}" className="border border-gray-300 rounded p-4">
          {comp_type} Component
        </div>""".format(comp_id=comp_id, comp_type=comp_type)
        
        return """import React from 'react';
import './App.css';

function App() {{
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">
          Generated React App
        </h1>
        <div className="space-y-4">
{component_jsx}
        </div>
      </div>
    </div>
  );
}}

export default App;""".format(component_jsx=component_jsx)
    
    def _generate_package_json(self) -> str:
        """Generates package.json with necessary dependencies."""
        return """{
  "name": "scribble-to-app",
  "version": "1.0.0",
  "description": "React app generated from UI sketch",
  "main": "index.js",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx,ts,tsx",
    "lint:fix": "eslint . --ext js,jsx,ts,tsx --fix"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.0",
    "autoprefixer": "^10.4.14",
    "eslint": "^8.45.0",
    "eslint-plugin-react": "^7.32.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.3",
    "postcss": "^8.4.24",
    "tailwindcss": "^3.3.2",
    "typescript": "^5.0.2",
    "vite": "^4.4.5"
  },
  "keywords": ["react", "tailwind", "ui", "generated"],
  "author": "Scribble2App",
  "license": "MIT"
}"""
    
    def _generate_tailwind_config(self) -> str:
        """Generates Tailwind CSS configuration."""
        return """/** @type {{import('tailwindcss').Config}} */
export default {{
  content: [
    "./index.html",
    "./src/**/*.{{js,ts,jsx,tsx}}",
  ],
  theme: {{
    extend: {{
      colors: {{
        primary: {{
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }}
      }},
      animation: {{
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      }},
      keyframes: {{
        fadeIn: {{
          '0%': {{ opacity: '0' }},
          '100%': {{ opacity: '1' }},
        }},
        slideUp: {{
          '0%': {{ transform: 'translateY(10px)', opacity: '0' }},
          '100%': {{ transform: 'translateY(0)', opacity: '1' }},
        }},
      }},
    }},
  }},
  plugins: [],
}}"""
    
    def _generate_index_html(self) -> str:
        """Generates the main HTML template."""
        return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Scribble2App - Generated React App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>"""
    
    def _generate_readme(self) -> str:
        """Generates README with setup instructions."""
        return """# Scribble2App - Generated React Application

This React application was automatically generated from a UI sketch using AI-powered code generation.

## Features

- 🎨 Modern UI with Tailwind CSS
- 📱 Responsive design
- ⚡ Fast development with Vite
- 🔧 TypeScript support
- ♿ Accessibility features

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint issues

## Project Structure

```
src/
├── App.jsx          # Main application component
├── main.jsx         # Application entry point
└── App.css          # Global styles
```

## Customization

You can customize the application by:

1. Modifying components in `src/App.jsx`
2. Updating Tailwind configuration in `tailwind.config.js`
3. Adding new components in the `src/components/` directory
4. Customizing colors and styling in the Tailwind config

## Technologies Used

- React 18
- Tailwind CSS
- Vite
- TypeScript
- ESLint

## License

MIT License - feel free to use this code for your projects!

---

Generated by Scribble2App - Convert sketches to code with AI ✨"""
    
    def create_project_zip(self, code_files: Dict[str, str], filename: str = None) -> str:
        """
        Creates a zip file containing the generated React project.
        
        Args:
            code_files: Dictionary of code files
            filename: Optional custom filename
            
        Returns:
            Path to the created zip file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"react_app_{timestamp}.zip"
        
        os.makedirs("temp", exist_ok=True)
        zip_path = os.path.join("temp", filename)
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Create project structure
                project_structure = {
                    'package.json': code_files.get('package_json', ''),
                    'tailwind.config.js': code_files.get('tailwind_config', ''),
                    'index.html': code_files.get('index_html', ''),
                    'README.md': code_files.get('readme_md', ''),
                    'src/App.jsx': code_files.get('app_jsx', ''),
                    'src/main.jsx': self._generate_main_jsx(),
                    'src/App.css': self._generate_app_css(),
                    'postcss.config.js': self._generate_postcss_config(),
                    'vite.config.js': self._generate_vite_config(),
                    'tsconfig.json': self._generate_tsconfig(),
                    '.eslintrc.cjs': self._generate_eslint_config(),
                }
                
                for file_path, content in project_structure.items():
                    zipf.writestr(file_path, content)
            
            return zip_path
            
        except Exception as e:
            st.error(f"Error creating zip file: {str(e)}")
            return None
    
    def _generate_main_jsx(self) -> str:
        """Generates the main.jsx entry point."""
        return """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)"""
    
    def _generate_app_css(self) -> str:
        """Generates global CSS styles."""
        return """@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom styles */
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

/* Smooth transitions */
* {
  transition: all 0.2s ease-in-out;
}

/* Custom component styles */
.btn-primary {
  @apply bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
}

.input-field {
  @apply border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500;
}"""
    
    def _generate_postcss_config(self) -> str:
        """Generates PostCSS configuration."""
        return """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}"""
    
    def _generate_vite_config(self) -> str:
        """Generates Vite configuration."""
        return """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})"""
    
    def _generate_tsconfig(self) -> str:
        """Generates TypeScript configuration."""
        return """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}"""
    
    def _generate_eslint_config(self) -> str:
        """Generates ESLint configuration."""
        return """module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
  },
}"""

# Example usage
if __name__ == "__main__":
    generator = ReactCodeGenerator()
    
    # Test with sample schema
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
    
    # Generate code (requires OpenAI API key)
    # code_files = generator.generate_react_code(test_schema)
    # print("Generated code files:", list(code_files.keys())) 