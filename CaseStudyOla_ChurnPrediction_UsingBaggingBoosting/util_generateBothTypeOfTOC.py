import json
import re
from pathlib import Path

def generate_toc_from_notebook(notebook_path, include_code_cells=False, max_depth=6, format_type='both'):
    """
    Generate a table of contents for a Jupyter notebook in markdown format.
    
    Args:
        notebook_path: Path to the .ipynb file
        include_code_cells: If True, includes code cells that start with # comments
        max_depth: Maximum heading depth to include (1-6)
        format_type: 'jupyter', 'vscode', or 'both'
    
    Returns:
        String containing the markdown TOC (or tuple of strings if format_type='both')
    """
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    toc_entries = []
    
    # Process each cell
    for cell_index, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            # Extract markdown headings
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            
            # Find all markdown headings
            for line in source.split('\n'):
                match = re.match(r'^(#{1,6})\s+(.+)$', line)
                if match:
                    level = len(match.group(1))
                    if level <= max_depth:
                        heading_text = match.group(2).strip()
                        toc_entries.append((level, heading_text, cell_index))
        
        elif include_code_cells and cell['cell_type'] == 'code':
            # Look for comment headings in code cells
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            
            for line in source.split('\n'):
                match = re.match(r'^#\s*(#{1,5})\s+(.+)$', line)
                if match:
                    level = len(match.group(1)) + 1  # +1 because we already have one #
                    if level <= max_depth:
                        heading_text = match.group(2).strip()
                        toc_entries.append((level, heading_text, cell_index))
    
    if format_type == 'jupyter':
        return format_toc_jupyter(toc_entries)
    elif format_type == 'vscode':
        return format_toc_vscode(toc_entries)
    else:  # both
        return format_toc_jupyter(toc_entries), format_toc_vscode(toc_entries)

def format_toc_vscode(toc_entries):
    """
    Format TOC entries into markdown list for VS Code.
    
    Args:
        toc_entries: List of tuples (level, text, cell_index)
    
    Returns:
        Formatted markdown string
    """
    if not toc_entries:
        return "No headings found in the notebook."
    
    toc_lines = ["# Table of Contents (VS Code)\n"]
    
    for level, text, _ in toc_entries:
        # Create anchor link from heading text
        anchor = create_anchor_vscode(text)
        
        # Create indented list item
        indent = "  " * (level - 1)
        toc_lines.append(f"{indent}- [{text}](#{anchor})")
    
    return '\n'.join(toc_lines)

def format_toc_jupyter(toc_entries):
    """
    Format TOC entries using HTML links for Jupyter Notebook.
    
    Args:
        toc_entries: List of tuples (level, text, cell_index)
    
    Returns:
        Formatted string with HTML links
    """
    if not toc_entries:
        return "No headings found in the notebook."
    
    toc_lines = ["# Table of Contents (Jupyter)\n"]
    
    for level, text, _ in toc_entries:
        # Create HTML anchor - replace spaces with hyphens
        anchor = text.strip().replace(' ', '-')
        
        # Create indentation using HTML spaces
        indent = "&nbsp;" * 4 * (level - 1)
        
        # Create HTML link
        toc_lines.append(f'{indent}• <a href="#{anchor}">{text}</a><br>')
    
    return '\n'.join(toc_lines)

def create_anchor_vscode(text):
    """
    Create anchor link from heading text following VS Code's convention.
    
    Args:
        text: Heading text
    
    Returns:
        Anchor string
    """
    # Remove markdown formatting
    text = re.sub(r'\*{1,2}([^\*]+)\*{1,2}', r'\1', text)  # Remove bold/italic
    text = re.sub(r'`([^`]+)`', r'\1', text)  # Remove code formatting
    text = re.sub(r'$$([^$$]+)\]$[^$]+\)', r'\1', text)  # Remove links
    
    # Convert to lowercase and replace spaces with hyphens
    anchor = text.lower()
    anchor = re.sub(r'[^\w\s-]', '', anchor)  # Remove non-alphanumeric chars
    anchor = re.sub(r'[-\s]+', '-', anchor)  # Replace spaces/multiple hyphens with single hyphen
    anchor = anchor.strip('-')  # Remove leading/trailing hyphens
    
    return anchor

def generate_both_tocs(notebook_path, include_code_cells=False, max_depth=6):
    """
    Generate both Jupyter and VS Code compatible TOCs.
    
    Args:
        notebook_path: Path to the .ipynb file
        include_code_cells: If True, includes code cells that start with # comments
        max_depth: Maximum heading depth to include (1-6)
    
    Returns:
        String containing both TOCs separated by a line
    """
    jupyter_toc, vscode_toc = generate_toc_from_notebook(
        notebook_path, include_code_cells, max_depth, format_type='both'
    )
    
    combined_toc = f"""## Table of Contents

**Note:** Use the appropriate TOC based on your environment:
- For **Jupyter Notebook**: Use the first TOC (with HTML links)
- For **VS Code**: Use the second TOC (with markdown links)

---

{jupyter_toc}

---

{vscode_toc}"""
    
    return combined_toc

def insert_toc_in_notebook(notebook_path, output_path=None, toc_title="Table of Contents", 
                          toc_format='both', include_code_cells=False, max_depth=6):
    """
    Insert a TOC at the beginning of a notebook (after the first cell if it's a title).
    
    Args:
        notebook_path: Path to the input notebook
        output_path: Path to save the modified notebook (if None, overwrites the original)
        toc_title: Title for the TOC
        toc_format: 'jupyter', 'vscode', or 'both'
        include_code_cells: If True, includes code cells that start with # comments
        max_depth: Maximum heading depth to include (1-6)
    """
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Generate TOC based on format
    if toc_format == 'both':
        toc_content = generate_both_tocs(notebook_path, include_code_cells, max_depth)
    else:
        toc_content = generate_toc_from_notebook(notebook_path, include_code_cells, max_depth, toc_format)
    
    # Check if first cell might be a title
    insert_position = 0
    if nb['cells'] and nb['cells'][0]['cell_type'] == 'markdown':
        first_cell_source = ''.join(nb['cells'][0]['source'])
        if re.match(r'^#\s+[^#]', first_cell_source):
            insert_position = 1
    
    # Create TOC cell
    toc_cell = {
        'cell_type': 'markdown',
        'metadata': {},
        'source': toc_content
    }
    
    # Insert TOC
    nb['cells'].insert(insert_position, toc_cell)
    
    # Save notebook
    if output_path is None:
        output_path = notebook_path
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2)
    
    print(f"TOC inserted at position {insert_position} in {output_path}")

def save_tocs_separately(notebook_path, include_code_cells=False, max_depth=6):
    """
    Generate and save both TOCs as separate markdown files.
    
    Args:
        notebook_path: Path to the .ipynb file
        include_code_cells: If True, includes code cells that start with # comments
        max_depth: Maximum heading depth to include (1-6)
    """
    jupyter_toc, vscode_toc = generate_toc_from_notebook(
        notebook_path, include_code_cells, max_depth, format_type='both'
    )
    
    # Save Jupyter TOC
    jupyter_file = Path(notebook_path).stem + "_toc_jupyter.md"
    with open(jupyter_file, 'w', encoding='utf-8') as f:
        f.write(jupyter_toc)
    print(f"Jupyter TOC saved to: {jupyter_file}")
    
    # Save VS Code TOC
    vscode_file = Path(notebook_path).stem + "_toc_vscode.md"
    with open(vscode_file, 'w', encoding='utf-8') as f:
        f.write(vscode_toc)
    print(f"VS Code TOC saved to: {vscode_file}")

# Example usage
if __name__ == "__main__":
    notebook_path = "Ola_AmitG.ipynb"
    
    # Option 1: Insert both TOCs in the notebook
    #insert_toc_in_notebook(notebook_path, output_path=notebook_path, toc_format='both')
    
    # Option 2: Insert only Jupyter TOC
    insert_toc_in_notebook(notebook_path, output_path=notebook_path, toc_format='jupyter')
    
    # Option 3: Insert only VS Code TOC
    # insert_toc_in_notebook(notebook_path, output_path=notebook_path, toc_format='vscode')
    
    # Option 4: Save TOCs as separate files
    # save_tocs_separately(notebook_path)