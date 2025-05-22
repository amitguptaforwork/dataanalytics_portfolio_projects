import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

class KPITreeGenerator:
    def __init__(self, figsize=(16, 12)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 8)
        self.ax.axis('off')
        
        # Color scheme
        self.colors = {
            'primary': '#FFA500',  # Orange for top KPI
            'secondary': '#1E90FF',  # Blue for main categories
            'tertiary': '#FFB6C1',  # Light pink for subcategories
            'quaternary': '#FF6347'  # Red-orange for actions
        }
    
    def draw_box(self, x, y, width, height, text, color, text_color='black', fontsize=10, bold=False):
        """Draw a rounded rectangle box with text"""
        box = FancyBboxPatch(
            (x - width/2, y - height/2), width, height,
            boxstyle=f"round,pad=0.05",
            facecolor=color,
            edgecolor='gray',
            linewidth=1
        )
        self.ax.add_patch(box)
        
        # Add text
        weight = 'bold' if bold else 'normal'
        self.ax.text(x, y, text, ha='center', va='center', 
                    fontsize=fontsize, color=text_color, weight=weight,
                    wrap=True)
    
    def draw_line(self, x1, y1, x2, y2, color='gray', linewidth=1):
        """Draw a connecting line"""
        self.ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth)
    
    def generate_kpi_tree(self, kpi_data):
        """
        Generate KPI tree from structured data
        
        kpi_data structure:
        {
            'top_kpi': {'name': 'KPI Name', 'description': 'Description'},
            'categories': [
                {
                    'name': 'Category Name',
                    'team': 'Team Name',
                    'metric': 'Metric Description',
                    'subcategories': [
                        {'name': 'Subcat1', 'type': 'normal'},
                        {'name': 'Subcat2', 'type': 'action'}
                    ]
                }
            ]
        }
        """
        
        # Draw top KPI
        top_kpi = kpi_data['top_kpi']
        self.draw_box(5, 7, 2.5, 0.8, f"{top_kpi['name']}\n{top_kpi['description']}", 
                     self.colors['primary'], fontsize=12, bold=True)
        
        # Draw "Owner" box
        self.draw_box(8.5, 7, 1, 0.5, "Owner\nKPI", 'black', 'white', fontsize=9)
        
        # Calculate positions for categories
        categories = kpi_data['categories']
        num_categories = len(categories)
        category_width = 8 / num_categories
        category_y = 5.5
        
        for i, category in enumerate(categories):
            x_pos = 1 + (i + 0.5) * category_width
            
            # Draw main category box
            self.draw_box(x_pos, category_y, 1.5, 1, 
                         f"{category['team']}\n{category['name']}", 
                         self.colors['secondary'], 'white', fontsize=10, bold=True)
            
            # Draw metric box below
            self.draw_box(x_pos, category_y - 1.5, 1.5, 0.8, 
                         category['metric'], 
                         'white', 'black', fontsize=9)
            
            # Connect to top KPI
            self.draw_line(5, 6.6, x_pos, category_y + 0.5)
            
            # Connect to metric box
            self.draw_line(x_pos, category_y - 0.5, x_pos, category_y - 1.1)
            
            # Draw subcategories if they exist
            if 'subcategories' in category:
                subcats = category['subcategories']
                num_subcats = len(subcats)
                subcat_start_x = x_pos - 0.6
                subcat_spacing = 1.2 / max(num_subcats - 1, 1) if num_subcats > 1 else 0
                
                for j, subcat in enumerate(subcats):
                    subcat_x = subcat_start_x + j * subcat_spacing if num_subcats > 1 else x_pos
                    subcat_y = 2.5
                    
                    # Choose color based on type
                    if subcat.get('type') == 'action':
                        color = self.colors['quaternary']
                        text_color = 'white'
                    else:
                        color = self.colors['tertiary']
                        text_color = 'black'
                    
                    self.draw_box(subcat_x, subcat_y, 0.8, 0.6, 
                                 subcat['name'], color, text_color, fontsize=8)
                    
                    # Connect to metric box
                    self.draw_line(x_pos, category_y - 1.9, subcat_x, subcat_y + 0.3)
        
        # Add level labels on the left
        self.ax.text(0.2, 7, 'TOP KPI', rotation=90, ha='center', va='center', 
                    fontsize=10, weight='bold', color='gray')
        self.ax.text(0.2, 5.5, 'CATEGORIES', rotation=90, ha='center', va='center', 
                    fontsize=10, weight='bold', color='gray')
        self.ax.text(0.2, 4, 'METRICS', rotation=90, ha='center', va='center', 
                    fontsize=10, weight='bold', color='gray')
        self.ax.text(0.2, 2.5, 'SUB-METRICS', rotation=90, ha='center', va='center', 
                    fontsize=10, weight='bold', color='gray')
        
        plt.tight_layout()
        return self.fig

# Example usage with your data
def create_example_diagram():
    kpi_data = {
        'top_kpi': {
            'name': 'COMPANY',
            'description': 'Weekly active subscribers (WAS)'
        },
        'categories': [
            {
                'name': 'REACH',
                'team': 'Marketing',
                'metric': 'Subscribers',
                'subcategories': [
                    {'name': 'Retained', 'type': 'normal'},
                    {'name': 'Reactivated', 'type': 'normal'},
                    {'name': 'New', 'type': 'normal'}
                ]
            },
            {
                'name': 'ACTIVATION',
                'team': 'Growth',
                'metric': 'Subscription in 7 days / New users',
                'subcategories': [
                    {'name': 'Time to subscription', 'type': 'normal'}
                ]
            },
            {
                'name': 'ENGAGEMENT',
                'team': 'Product & Content',
                'metric': 'Minutes watched / WAS',
                'subcategories': [
                    {'name': 'Product\nVideo starts / WAS', 'type': 'action'},
                    {'name': 'Content\nComplete / Start', 'type': 'action'},
                    {'name': 'Content\nSame show retention', 'type': 'action'}
                ]
            },
            {
                'name': 'RETENTION',
                'team': 'Product & Marketing',
                'metric': '1-week WAS retention'
            },
            {
                'name': 'BUSINESS-SPECIFIC',
                'team': 'Product',
                'metric': 'Avg. revenue / Subscriber'
            }
        ]
    }
    
    generator = KPITreeGenerator()
    fig = generator.generate_kpi_tree(kpi_data)
    plt.show()
    return fig

# Mermaid diagram generator
def generate_mermaid_diagram(kpi_data):
    """Generate Mermaid diagram code for the KPI tree"""
    mermaid_code = "graph TD\n"
    
    # Top KPI
    top_kpi = kpi_data['top_kpi']
    mermaid_code += f'    A["{top_kpi["name"]}<br/>{top_kpi["description"]}"] --> B["Owner<br/>KPI"]\n'
    
    # Categories
    for i, category in enumerate(kpi_data['categories']):
        cat_id = chr(67 + i)  # C, D, E, etc.
        mermaid_code += f'    A --> {cat_id}["{category["team"]}<br/>{category["name"]}"]\n'
        
        # Metric
        metric_id = f"{cat_id}1"
        mermaid_code += f'    {cat_id} --> {metric_id}["{category["metric"]}"]\n'
        
        # Subcategories
        if 'subcategories' in category:
            for j, subcat in enumerate(category['subcategories']):
                subcat_id = f"{cat_id}{j + 2}"
                mermaid_code += f'    {metric_id} --> {subcat_id}["{subcat["name"]}"]\n'
    
    return mermaid_code

# Example usage
if __name__ == "__main__":
    # Create the matplotlib version
    fig = create_example_diagram()
    
    # Generate Mermaid code
    kpi_data = {
        'top_kpi': {'name': 'COMPANY', 'description': 'Weekly active subscribers (WAS)'},
        'categories': [
            {
                'name': 'REACH', 'team': 'Marketing', 'metric': 'Subscribers',
                'subcategories': [
                    {'name': 'Retained'}, {'name': 'Reactivated'}, {'name': 'New'}
                ]
            },
            {
                'name': 'ACTIVATION', 'team': 'Growth', 
                'metric': 'Subscription in 7 days / New users',
                'subcategories': [{'name': 'Time to subscription'}]
            }
        ]
    }
    
    mermaid_code = generate_mermaid_diagram(kpi_data)
    print("Mermaid Diagram Code:")
    print(mermaid_code)