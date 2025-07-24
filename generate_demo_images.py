#!/usr/bin/env python3
"""
Demo Image Generator for Scribble2App README
Generates high-quality demo images showing the application workflow.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

class DemoImageGenerator:
    def __init__(self):
        self.output_dir = "demo_images"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Color scheme
        self.colors = {
            'primary': '#2563eb',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'info': '#06b6d4',
            'light': '#f8fafc',
            'dark': '#1e293b',
            'gray': '#64748b'
        }
    
    def create_upload_interface_demo(self):
        """Create demo image for upload interface."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        fig.patch.set_facecolor(self.colors['light'])
        
        # Main container
        container = patches.Rectangle((1, 1), 10, 6, 
                                    facecolor='white', 
                                    edgecolor=self.colors['gray'], 
                                    linewidth=2,
                                    alpha=0.9)
        ax.add_patch(container)
        
        # Title
        ax.text(6, 6.5, 'Scribble2App - Upload Interface', 
               fontsize=20, fontweight='bold', 
               ha='center', color=self.colors['dark'])
        
        # Upload area
        upload_area = patches.Rectangle((2, 3.5), 8, 2.5, 
                                      facecolor=self.colors['light'], 
                                      edgecolor=self.colors['primary'], 
                                      linewidth=3,
                                      linestyle='--')
        ax.add_patch(upload_area)
        
        # Upload icon
        ax.text(6, 4.75, '📁', fontsize=40, ha='center')
        ax.text(6, 4.25, 'Drag & Drop or Click to Upload', 
               fontsize=14, ha='center', color=self.colors['gray'])
        ax.text(6, 3.9, 'Supports: PNG, JPG, JPEG, BMP, TIFF', 
               fontsize=10, ha='center', color=self.colors['gray'])
        
        # Sidebar
        sidebar = patches.Rectangle((0.5, 1), 0.8, 6, 
                                  facecolor=self.colors['primary'], 
                                  alpha=0.8)
        ax.add_patch(sidebar)
        
        # Sidebar items
        sidebar_items = ['Upload', 'Detect', 'Extract', 'Schema', 'Generate', 'Download']
        for i, item in enumerate(sidebar_items):
            y_pos = 6.5 - i * 0.8
            ax.text(0.9, y_pos, item, fontsize=10, 
                   color='white', fontweight='bold', ha='center')
        
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/upload_interface.png', 
                   dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['light'])
        plt.close()
    
    def create_element_detection_demo(self):
        """Create demo image for element detection."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        fig.patch.set_facecolor(self.colors['light'])
        
        # Main container
        container = patches.Rectangle((1, 1), 10, 6, 
                                    facecolor='white', 
                                    edgecolor=self.colors['gray'], 
                                    linewidth=2,
                                    alpha=0.9)
        ax.add_patch(container)
        
        # Title
        ax.text(6, 6.5, 'Element Detection Results', 
               fontsize=20, fontweight='bold', 
               ha='center', color=self.colors['dark'])
        
        # Sample sketch
        sketch_area = patches.Rectangle((1.5, 3.5), 4, 2.5, 
                                      facecolor='white', 
                                      edgecolor=self.colors['gray'], 
                                      linewidth=1)
        ax.add_patch(sketch_area)
        
        # Draw simple UI elements in sketch
        # Button
        button = patches.Rectangle((2, 4.5), 2, 0.5, 
                                 facecolor=self.colors['success'], 
                                 alpha=0.3,
                                 edgecolor=self.colors['success'],
                                 linewidth=2)
        ax.add_patch(button)
        ax.text(3, 4.75, 'Submit', fontsize=10, ha='center', fontweight='bold')
        
        # Input field
        input_field = patches.Rectangle((2, 5.2), 2, 0.4, 
                                      facecolor='white', 
                                      edgecolor=self.colors['gray'],
                                      linewidth=1)
        ax.add_patch(input_field)
        ax.text(2.2, 5.4, 'Email', fontsize=8, color=self.colors['gray'])
        
        # Detection results
        results_area = patches.Rectangle((6.5, 3.5), 4, 2.5, 
                                       facecolor=self.colors['light'], 
                                       edgecolor=self.colors['info'],
                                       linewidth=2)
        ax.add_patch(results_area)
        
        # Detection list
        detections = [
            ('Button', 'Submit', '98%'),
            ('Input', 'Email', '95%'),
            ('Label', 'Email', '92%'),
            ('Container', 'Form', '89%')
        ]
        
        for i, (element, text, confidence) in enumerate(detections):
            y_pos = 5.5 - i * 0.4
            ax.text(6.8, y_pos, f'{element}: {text}', 
                   fontsize=10, fontweight='bold')
            ax.text(9.8, y_pos, confidence, 
                   fontsize=10, color=self.colors['success'])
        
        ax.text(6.8, 3.8, 'Detected Elements:', 
               fontsize=12, fontweight='bold', color=self.colors['dark'])
        
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/element_detection.png', 
                   dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['light'])
        plt.close()
    
    def create_text_extraction_demo(self):
        """Create demo image for text extraction."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        fig.patch.set_facecolor(self.colors['light'])
        
        # Main container
        container = patches.Rectangle((1, 1), 10, 6, 
                                    facecolor='white', 
                                    edgecolor=self.colors['gray'], 
                                    linewidth=2,
                                    alpha=0.9)
        ax.add_patch(container)
        
        # Title
        ax.text(6, 6.5, 'Text Extraction Results', 
               fontsize=20, fontweight='bold', 
               ha='center', color=self.colors['dark'])
        
        # Original image with text
        original_area = patches.Rectangle((1.5, 3.5), 4, 2.5, 
                                        facecolor='white', 
                                        edgecolor=self.colors['gray'], 
                                        linewidth=1)
        ax.add_patch(original_area)
        
        # Simulate handwritten text
        ax.text(2, 5.5, 'Login', fontsize=16, fontweight='bold', 
               style='italic', color=self.colors['dark'])
        ax.text(2, 5, 'Email:', fontsize=12, style='italic')
        ax.text(2, 4.5, 'Password:', fontsize=12, style='italic')
        ax.text(3, 4, 'Submit', fontsize=14, fontweight='bold', 
               style='italic', color=self.colors['success'])
        
        # Extracted text results
        results_area = patches.Rectangle((6.5, 3.5), 4, 2.5, 
                                       facecolor=self.colors['light'], 
                                       edgecolor=self.colors['warning'],
                                       linewidth=2)
        ax.add_patch(results_area)
        
        # OCR results
        ocr_results = [
            ('Login', '98%'),
            ('Email:', '95%'),
            ('Password:', '92%'),
            ('Submit', '96%')
        ]
        
        ax.text(6.8, 5.5, 'Extracted Text:', 
               fontsize=12, fontweight='bold', color=self.colors['dark'])
        
        for i, (text, confidence) in enumerate(ocr_results):
            y_pos = 5 - i * 0.4
            ax.text(6.8, y_pos, f'"{text}"', 
                   fontsize=10, fontweight='bold')
            ax.text(9.8, y_pos, confidence, 
                   fontsize=10, color=self.colors['warning'])
        
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/text_extraction.png', 
                   dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['light'])
        plt.close()
    
    def create_schema_building_demo(self):
        """Create demo image for schema building."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        fig.patch.set_facecolor(self.colors['light'])
        
        # Main container
        container = patches.Rectangle((1, 1), 10, 6, 
                                    facecolor='white', 
                                    edgecolor=self.colors['gray'], 
                                    linewidth=2,
                                    alpha=0.9)
        ax.add_patch(container)
        
        # Title
        ax.text(6, 6.5, 'UI Schema Generation', 
               fontsize=20, fontweight='bold', 
               ha='center', color=self.colors['dark'])
        
        # Schema tree visualization
        # Root
        ax.text(6, 5.5, 'LoginForm', fontsize=14, fontweight='bold', 
               ha='center', color=self.colors['primary'])
        
        # Children
        children = [
            ('Header', 4, 4.8),
            ('Form', 6, 4.8),
            ('Footer', 8, 4.8)
        ]
        
        for child, x, y in children:
            ax.text(x, y, child, fontsize=12, fontweight='bold', 
                   ha='center', color=self.colors['info'])
            # Connection line
            ax.plot([6, x], [5.3, y+0.2], color=self.colors['gray'], 
                   linewidth=1, alpha=0.7)
        
        # Form children
        form_children = [
            ('EmailInput', 5, 3.8),
            ('PasswordInput', 6, 3.8),
            ('SubmitButton', 7, 3.8)
        ]
        
        for child, x, y in form_children:
            ax.text(x, y, child, fontsize=10, fontweight='bold', 
                   ha='center', color=self.colors['success'])
            # Connection line
            ax.plot([6, x], [4.6, y+0.2], color=self.colors['gray'], 
                   linewidth=1, alpha=0.7)
        
        # Schema properties
        properties_area = patches.Rectangle((1.5, 2), 9, 1.5, 
                                          facecolor=self.colors['light'], 
                                          edgecolor=self.colors['info'],
                                          linewidth=2)
        ax.add_patch(properties_area)
        
        ax.text(1.8, 3.2, 'Schema Properties:', 
               fontsize=12, fontweight='bold', color=self.colors['dark'])
        
        properties = [
            'Layout: Vertical Stack',
            'Components: 6',
            'Responsive: Yes',
            'Accessibility: WCAG 2.1'
        ]
        
        for i, prop in enumerate(properties):
            y_pos = 2.8 - i * 0.2
            ax.text(1.8, y_pos, prop, fontsize=10)
        
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/schema_building.png', 
                   dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['light'])
        plt.close()
    
    def create_code_generation_demo(self):
        """Create demo image for code generation."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        fig.patch.set_facecolor(self.colors['light'])
        
        # Main container
        container = patches.Rectangle((1, 1), 10, 6, 
                                    facecolor='white', 
                                    edgecolor=self.colors['gray'], 
                                    linewidth=2,
                                    alpha=0.9)
        ax.add_patch(container)
        
        # Title
        ax.text(6, 6.5, 'React Code Generation', 
               fontsize=20, fontweight='bold', 
               ha='center', color=self.colors['dark'])
        
        # Code editor simulation
        code_area = patches.Rectangle((1.5, 2), 9, 3.5, 
                                    facecolor='#1e1e1e', 
                                    edgecolor=self.colors['gray'],
                                    linewidth=2)
        ax.add_patch(code_area)
        
        # Code content
        code_lines = [
            'function LoginForm() {',
            '  return (',
            '    <div className="min-h-screen bg-gray-100">',
            '      <div className="bg-white p-8 rounded-lg">',
            '        <h1 className="text-2xl font-bold">Login</h1>',
            '        <form className="space-y-4">',
            '          <input type="email" placeholder="Email" />',
            '          <input type="password" placeholder="Password" />',
            '          <button type="submit">Submit</button>',
            '        </form>',
            '      </div>',
            '    </div>',
            '  );',
            '}'
        ]
        
        for i, line in enumerate(code_lines):
            y_pos = 5.2 - i * 0.2
            color = '#d4d4d4' if i < 2 else '#9cdcfe' if 'function' in line else '#d7ba7d' if 'className' in line else '#d4d4d4'
            ax.text(1.8, y_pos, line, fontsize=9, 
                   fontfamily='monospace', color=color)
        
        # Status indicators
        ax.text(1.8, 1.5, '✓ React Component Generated', 
               fontsize=10, color=self.colors['success'], fontweight='bold')
        ax.text(4, 1.5, '✓ Tailwind CSS Styled', 
               fontsize=10, color=self.colors['success'], fontweight='bold')
        ax.text(6.5, 1.5, '✓ Responsive Design', 
               fontsize=10, color=self.colors['success'], fontweight='bold')
        
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/code_generation.png', 
                   dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['light'])
        plt.close()
    
    def create_download_results_demo(self):
        """Create demo image for download results."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        fig.patch.set_facecolor(self.colors['light'])
        
        # Main container
        container = patches.Rectangle((1, 1), 10, 6, 
                                    facecolor='white', 
                                    edgecolor=self.colors['gray'], 
                                    linewidth=2,
                                    alpha=0.9)
        ax.add_patch(container)
        
        # Title
        ax.text(6, 6.5, 'Download Generated Project', 
               fontsize=20, fontweight='bold', 
               ha='center', color=self.colors['dark'])
        
        # File structure
        file_area = patches.Rectangle((1.5, 2), 9, 3.5, 
                                    facecolor=self.colors['light'], 
                                    edgecolor=self.colors['success'],
                                    linewidth=2)
        ax.add_patch(file_area)
        
        # File tree
        files = [
            '📁 login-app/',
            '  📄 package.json',
            '  📄 README.md',
            '  📁 src/',
            '    📄 App.js',
            '    📄 LoginForm.js',
            '    📄 index.js',
            '  📁 public/',
            '    📄 index.html',
            '  📄 tailwind.config.js'
        ]
        
        for i, file in enumerate(files):
            y_pos = 5.2 - i * 0.25
            color = self.colors['primary'] if '📁' in file else self.colors['dark']
            ax.text(1.8, y_pos, file, fontsize=10, color=color)
        
        # Download button
        download_btn = patches.Rectangle((4, 1.2), 4, 0.6, 
                                       facecolor=self.colors['success'], 
                                       edgecolor=self.colors['success'],
                                       linewidth=2)
        ax.add_patch(download_btn)
        ax.text(6, 1.5, '📥 Download Project', 
               fontsize=14, fontweight='bold', 
               ha='center', color='white')
        
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/download_results.png', 
                   dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['light'])
        plt.close()
    
    def create_main_demo(self):
        """Create the main demo image."""
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))
        fig.patch.set_facecolor(self.colors['light'])
        
        # Title
        ax.text(8, 9.5, 'Scribble2App - AI-Powered Sketch to Code', 
               fontsize=24, fontweight='bold', 
               ha='center', color=self.colors['dark'])
        
        # Workflow diagram
        steps = [
            ('Upload\nSketch', 2, 7, self.colors['primary']),
            ('Detect\nElements', 4, 7, self.colors['info']),
            ('Extract\nText', 6, 7, self.colors['warning']),
            ('Build\nSchema', 8, 7, self.colors['danger']),
            ('Generate\nCode', 10, 7, self.colors['success'])
        ]
        
        # Draw steps
        for text, x, y, color in steps:
            circle = patches.Circle((x, y), 0.8, 
                                  facecolor=color, 
                                  edgecolor='white',
                                  linewidth=3)
            ax.add_patch(circle)
            ax.text(x, y, text, fontsize=10, fontweight='bold', 
                   ha='center', va='center', color='white')
        
        # Connect steps with arrows
        for i in range(len(steps) - 1):
            x1, y1 = steps[i][1], steps[i][2]
            x2, y2 = steps[i+1][1], steps[i+1][2]
            ax.annotate('', xy=(x2-0.5, y2), xytext=(x1+0.5, y1),
                       arrowprops=dict(arrowstyle='->', lw=2, color=self.colors['gray']))
        
        # Before/After comparison
        # Before sketch
        before_area = patches.Rectangle((1, 2), 6, 4, 
                                      facecolor='white', 
                                      edgecolor=self.colors['gray'], 
                                      linewidth=2)
        ax.add_patch(before_area)
        ax.text(4, 6.5, 'Hand-drawn Sketch', 
               fontsize=14, fontweight='bold', ha='center')
        
        # Simple sketch
        ax.text(2.5, 5.5, 'Login', fontsize=16, fontweight='bold', 
               style='italic', color=self.colors['dark'])
        ax.text(2.5, 5, 'Email: [______]', fontsize=12, style='italic')
        ax.text(2.5, 4.5, 'Password: [______]', fontsize=12, style='italic')
        ax.text(3.5, 4, 'Submit', fontsize=14, fontweight='bold', 
               style='italic', color=self.colors['success'])
        
        # After code
        after_area = patches.Rectangle((9, 2), 6, 4, 
                                     facecolor='white', 
                                     edgecolor=self.colors['gray'], 
                                     linewidth=2)
        ax.add_patch(after_area)
        ax.text(12, 6.5, 'Generated React App', 
               fontsize=14, fontweight='bold', ha='center')
        
        # Code preview
        code_lines = [
            'function LoginForm() {',
            '  return (',
            '    <div className="bg-white p-8">',
            '      <h1>Login</h1>',
            '      <form>',
            '        <input type="email" />',
            '        <input type="password" />',
            '        <button>Submit</button>',
            '      </form>',
            '    </div>',
            '  );',
            '}'
        ]
        
        for i, line in enumerate(code_lines):
            y_pos = 5.8 - i * 0.25
            ax.text(9.2, y_pos, line, fontsize=8, 
                   fontfamily='monospace', color=self.colors['dark'])
        
        # Arrow between before/after
        ax.annotate('', xy=(8.5, 4), xytext=(7.5, 4),
                   arrowprops=dict(arrowstyle='->', lw=3, color=self.colors['primary']))
        
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/main_demo.png', 
                   dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['light'])
        plt.close()
    
    def generate_all_demos(self):
        """Generate all demo images."""
        print("Generating demo images...")
        
        self.create_main_demo()
        print("✓ Main demo image created")
        
        self.create_upload_interface_demo()
        print("✓ Upload interface demo created")
        
        self.create_element_detection_demo()
        print("✓ Element detection demo created")
        
        self.create_text_extraction_demo()
        print("✓ Text extraction demo created")
        
        self.create_schema_building_demo()
        print("✓ Schema building demo created")
        
        self.create_code_generation_demo()
        print("✓ Code generation demo created")
        
        self.create_download_results_demo()
        print("✓ Download results demo created")
        
        print(f"\nAll demo images saved to '{self.output_dir}/' directory")
        print("You can now update the README.md with these image paths")

def main():
    """Main function to generate all demo images."""
    generator = DemoImageGenerator()
    generator.generate_all_demos()

if __name__ == "__main__":
    main() 