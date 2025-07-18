import json
import streamlit as st
import os
from typing import List, Dict, Any
import math

class UISchemaBuilder:
    """Converts detected UI elements and text into a structured schema for code generation."""
    
    def __init__(self):
        self.layout_types = ['flex', 'grid', 'stack', 'sidebar']
        self.component_mapping = {
            'button': 'Button',
            'input': 'Input',
            'text': 'Text',
            'image': 'Image',
            'checkbox': 'Checkbox',
            'radio': 'Radio',
            'dropdown': 'Select',
            'textarea': 'Textarea',
            'link': 'Link',
            'header': 'Header',
            'footer': 'Footer',
            'sidebar': 'Sidebar',
            'card': 'Card',
            'modal': 'Modal',
            'table': 'Table'
        }
    
    def build_schema(self, detected_elements: List[Dict], text_regions: List[Dict], image_size: tuple) -> Dict[str, Any]:
        """
        Builds a comprehensive UI schema from detected elements and text.
        
        Args:
            detected_elements: List of detected UI elements with bounding boxes
            text_regions: List of text regions with bounding boxes
            image_size: Tuple of (width, height) of the original image
            
        Returns:
            Structured UI schema dictionary
        """
        try:
            # Initialize schema
            schema = {
                'metadata': {
                    'image_size': image_size,
                    'total_elements': len(detected_elements),
                    'total_text_regions': len(text_regions)
                },
                'layout': self._determine_layout(detected_elements, image_size),
                'components': [],
                'styling': {
                    'theme': 'default',
                    'colors': self._extract_colors(detected_elements),
                    'spacing': self._calculate_spacing(detected_elements)
                }
            }
            
            # Process detected elements
            for element in detected_elements:
                component = self._create_component_from_element(element, text_regions)
                if component:
                    schema['components'].append(component)
            
            # Add standalone text regions
            standalone_text = self._find_standalone_text(text_regions, detected_elements)
            for text_region in standalone_text:
                component = self._create_text_component(text_region)
                if component:
                    schema['components'].append(component)
            
            # Sort components by position (top to bottom, left to right)
            schema['components'].sort(key=lambda x: (x['position']['y'], x['position']['x']))
            
            # Add layout containers
            schema['containers'] = self._create_containers(schema['components'])
            
            return schema
            
        except Exception as e:
            st.error(f"Error building schema: {str(e)}")
            return self._create_fallback_schema(detected_elements, text_regions, image_size)
    
    def _determine_layout(self, elements: List[Dict], image_size: tuple) -> str:
        """
        Determines the overall layout type based on element positions.
        
        Args:
            elements: List of detected elements
            image_size: Image dimensions
            
        Returns:
            Layout type string
        """
        if not elements:
            return 'flex'
        
        # Analyze element positions
        x_positions = [elem['center'][0] for elem in elements]
        y_positions = [elem['center'][1] for elem in elements]
        
        width, height = image_size
        
        # Check for grid-like arrangement
        x_variance = self._calculate_variance(x_positions)
        y_variance = self._calculate_variance(y_positions)
        
        if x_variance > width * 0.3 and y_variance > height * 0.3:
            return 'grid'
        elif max(x_positions) - min(x_positions) > width * 0.7:
            return 'flex'
        else:
            return 'stack'
    
    def _create_component_from_element(self, element: Dict, text_regions: List[Dict]) -> Dict[str, Any]:
        """
        Creates a component schema from a detected element.
        
        Args:
            element: Detected UI element
            text_regions: List of text regions for text extraction
            
        Returns:
            Component schema dictionary
        """
        bbox = element['bbox']
        element_type = element['type']
        
        # Find associated text
        associated_text = self._find_associated_text(bbox, text_regions)
        
        # Create component
        component = {
            'type': self.component_mapping.get(element_type, 'Element'),
            'id': f"{element_type}_{len(bbox)}",
            'position': {
                'x': bbox[0],
                'y': bbox[1],
                'width': bbox[2] - bbox[0],
                'height': bbox[3] - bbox[1]
            },
            'props': {},
            'styling': {}
        }
        
        # Add type-specific properties
        if element_type == 'button':
            component['props']['text'] = associated_text or 'Button'
            component['props']['onClick'] = 'handleClick'
        elif element_type == 'input':
            component['props']['placeholder'] = associated_text or 'Enter text...'
            component['props']['type'] = 'text'
        elif element_type == 'textarea':
            component['props']['placeholder'] = associated_text or 'Enter text...'
            component['props']['rows'] = 3
        elif element_type == 'checkbox':
            component['props']['label'] = associated_text or 'Checkbox'
        elif element_type == 'radio':
            component['props']['label'] = associated_text or 'Radio'
        elif element_type == 'dropdown':
            component['props']['placeholder'] = associated_text or 'Select option...'
            component['props']['options'] = ['Option 1', 'Option 2', 'Option 3']
        elif element_type == 'link':
            component['props']['text'] = associated_text or 'Link'
            component['props']['href'] = '#'
        elif element_type == 'text':
            component['props']['text'] = associated_text or 'Text'
        elif element_type == 'image':
            component['props']['src'] = '/placeholder-image.jpg'
            component['props']['alt'] = associated_text or 'Image'
        
        # Add styling based on element type
        component['styling'] = self._get_default_styling(element_type)
        
        return component
    
    def _create_text_component(self, text_region: Dict) -> Dict[str, Any]:
        """
        Creates a text component from a text region.
        
        Args:
            text_region: Text region with bounding box and text
            
        Returns:
            Text component schema
        """
        bbox = text_region['bbox']
        text = text_region['text']
        
        return {
            'type': 'Text',
            'id': f"text_{len(text)}",
            'position': {
                'x': bbox[0],
                'y': bbox[1],
                'width': bbox[2] - bbox[0],
                'height': bbox[3] - bbox[1]
            },
            'props': {
                'text': text
            },
            'styling': {
                'fontSize': '16px',
                'fontWeight': 'normal',
                'color': '#333333'
            }
        }
    
    def _find_associated_text(self, bbox: List[int], text_regions: List[Dict]) -> str:
        """
        Finds text associated with a UI element based on proximity.
        
        Args:
            bbox: Bounding box of the element
            text_regions: List of text regions
            
        Returns:
            Associated text string
        """
        element_center = [(bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2]
        element_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
        
        best_match = None
        best_distance = float('inf')
        
        for text_region in text_regions:
            text_bbox = text_region['bbox']
            text_center = text_region['center']
            
            # Calculate distance between centers
            distance = math.sqrt(
                (element_center[0] - text_center[0]) ** 2 + 
                (element_center[1] - text_center[1]) ** 2
            )
            
            # Check if text is within or very close to the element
            if (text_bbox[0] >= bbox[0] and text_bbox[1] >= bbox[1] and 
                text_bbox[2] <= bbox[2] and text_bbox[3] <= bbox[3]):
                return text_region['text']
            
            # Find closest text within reasonable distance
            if distance < element_area * 0.1 and distance < best_distance:
                best_match = text_region['text']
                best_distance = distance
        
        return best_match
    
    def _find_standalone_text(self, text_regions: List[Dict], elements: List[Dict]) -> List[Dict]:
        """
        Finds text regions that are not associated with any UI elements.
        
        Args:
            text_regions: List of text regions
            elements: List of detected elements
            
        Returns:
            List of standalone text regions
        """
        standalone = []
        
        for text_region in text_regions:
            text_bbox = text_region['bbox']
            is_associated = False
            
            for element in elements:
                element_bbox = element['bbox']
                
                # Check if text is within element bounds
                if (text_bbox[0] >= element_bbox[0] and text_bbox[1] >= element_bbox[1] and 
                    text_bbox[2] <= element_bbox[2] and text_bbox[3] <= element_bbox[3]):
                    is_associated = True
                    break
            
            if not is_associated:
                standalone.append(text_region)
        
        return standalone
    
    def _get_default_styling(self, element_type: str) -> Dict[str, str]:
        """
        Returns default styling for different element types.
        
        Args:
            element_type: Type of UI element
            
        Returns:
            Default styling dictionary
        """
        base_styles = {
            'margin': '8px',
            'padding': '8px',
            'borderRadius': '4px'
        }
        
        if element_type == 'button':
            return {
                **base_styles,
                'backgroundColor': '#007bff',
                'color': 'white',
                'border': 'none',
                'cursor': 'pointer'
            }
        elif element_type == 'input':
            return {
                **base_styles,
                'border': '1px solid #ccc',
                'backgroundColor': 'white'
            }
        elif element_type == 'text':
            return {
                **base_styles,
                'fontSize': '16px',
                'color': '#333333'
            }
        else:
            return base_styles
    
    def _extract_colors(self, elements: List[Dict]) -> Dict[str, str]:
        """
        Extracts color scheme from detected elements.
        
        Args:
            elements: List of detected elements
            
        Returns:
            Color scheme dictionary
        """
        # For now, return a default color scheme
        # In a full implementation, you'd analyze the image colors
        return {
            'primary': '#007bff',
            'secondary': '#6c757d',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }
    
    def _calculate_spacing(self, elements: List[Dict]) -> Dict[str, int]:
        """
        Calculates spacing between elements.
        
        Args:
            elements: List of detected elements
            
        Returns:
            Spacing configuration
        """
        if len(elements) < 2:
            return {'margin': 8, 'padding': 8, 'gap': 16}
        
        # Calculate average spacing between elements
        spacings = []
        for i in range(len(elements) - 1):
            elem1 = elements[i]
            elem2 = elements[i + 1]
            
            # Calculate vertical spacing
            if elem1['bbox'][1] < elem2['bbox'][1]:
                spacing = elem2['bbox'][1] - elem1['bbox'][3]
                if spacing > 0:
                    spacings.append(spacing)
        
        avg_spacing = sum(spacings) // len(spacings) if spacings else 16
        
        return {
            'margin': avg_spacing // 2,
            'padding': avg_spacing // 2,
            'gap': avg_spacing
        }
    
    def _create_containers(self, components: List[Dict]) -> List[Dict]:
        """
        Creates layout containers to group related components.
        
        Args:
            components: List of components
            
        Returns:
            List of container schemas
        """
        containers = []
        
        # Group components by vertical position
        if len(components) > 1:
            # Simple grouping: create a main container
            main_container = {
                'type': 'Container',
                'id': 'main_container',
                'layout': 'flex',
                'direction': 'column',
                'children': [comp['id'] for comp in components],
                'styling': {
                    'padding': '20px',
                    'gap': '16px'
                }
            }
            containers.append(main_container)
        
        return containers
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculates variance of a list of values."""
        if not values:
            return 0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def _create_fallback_schema(self, elements: List[Dict], text_regions: List[Dict], image_size: tuple) -> Dict[str, Any]:
        """
        Creates a fallback schema when the main schema building fails.
        
        Args:
            elements: List of detected elements
            text_regions: List of text regions
            image_size: Image dimensions
            
        Returns:
            Basic fallback schema
        """
        return {
            'metadata': {
                'image_size': image_size,
                'total_elements': len(elements),
                'total_text_regions': len(text_regions)
            },
            'layout': 'flex',
            'components': [
                {
                    'type': 'Text',
                    'id': 'fallback_text',
                    'position': {'x': 0, 'y': 0, 'width': 100, 'height': 50},
                    'props': {'text': 'UI Components Detected'},
                    'styling': {'fontSize': '16px', 'color': '#333333'}
                }
            ],
            'containers': [],
            'styling': {
                'theme': 'default',
                'colors': {'primary': '#007bff'},
                'spacing': {'margin': 8, 'padding': 8, 'gap': 16}
            }
        }
    
    def save_schema(self, schema: Dict[str, Any], filename: str = "ui_schema.json") -> str:
        """
        Saves the UI schema to a JSON file.
        
        Args:
            schema: UI schema dictionary
            filename: Name of the output file
            
        Returns:
            Path to the saved file
        """
        os.makedirs("temp", exist_ok=True)
        file_path = os.path.join("temp", filename)
        
        with open(file_path, 'w') as f:
            json.dump(schema, f, indent=2)
        
        return file_path
    
    def validate_schema(self, schema: Dict[str, Any]) -> bool:
        """
        Validates the generated schema for completeness and correctness.
        
        Args:
            schema: UI schema dictionary
            
        Returns:
            True if schema is valid, False otherwise
        """
        required_keys = ['metadata', 'layout', 'components']
        
        # Check required keys
        for key in required_keys:
            if key not in schema:
                st.error(f"Missing required key in schema: {key}")
                return False
        
        # Check components
        if not isinstance(schema['components'], list):
            st.error("Components must be a list")
            return False
        
        # Validate each component
        for i, component in enumerate(schema['components']):
            if not self._validate_component(component, i):
                return False
        
        return True
    
    def _validate_component(self, component: Dict, index: int) -> bool:
        """
        Validates a single component in the schema.
        
        Args:
            component: Component dictionary
            index: Component index for error reporting
            
        Returns:
            True if component is valid, False otherwise
        """
        required_keys = ['type', 'id', 'position', 'props']
        
        for key in required_keys:
            if key not in component:
                st.error(f"Component {index} missing required key: {key}")
                return False
        
        # Validate position
        position = component['position']
        required_position_keys = ['x', 'y', 'width', 'height']
        
        for key in required_position_keys:
            if key not in position:
                st.error(f"Component {index} position missing key: {key}")
                return False
        
        return True

# Example usage
if __name__ == "__main__":
    builder = UISchemaBuilder()
    
    # Test with sample data
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
    
    schema = builder.build_schema(test_elements, test_text_regions, (600, 400))
    print("Generated Schema:")
    print(json.dumps(schema, indent=2)) 