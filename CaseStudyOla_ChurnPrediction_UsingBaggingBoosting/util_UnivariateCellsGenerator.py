import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

def create_analysis_notebook(num_cols, cat_cols, output_filename='analysis_notebook.ipynb'):
    """
    Creates a new Jupyter notebook with analysis cells for numerical and categorical columns
    
    Parameters:
    num_cols: list of numerical column names
    cat_cols: list of categorical column names (for future use)
    output_filename: name of the output notebook file
    """
    
    # Create a new notebook
    nb = new_notebook()
    cells = []
    
    # Add a title cell (optional)
    title_cell = new_markdown_cell("# Data Analysis Notebook\n\n## Numerical Columns Analysis")
    cells.append(title_cell)
    
    # For each numerical column, create markdown and code cells
    for col_name in num_cols:
        # Create markdown cell with column name as heading
        markdown_content = f"### {col_name}"
        markdown_cell = new_markdown_cell(markdown_content)
        cells.append(markdown_cell)
        
        # Create code cell with analysis code
        code_content = f'''col = '{col_name}'

univariate_numerical_analysis(df[col], f"{{col}} Data")'''
        code_cell = new_code_cell(code_content)
        cells.append(code_cell)
    
    # For each numerical column, create markdown and code cells
    for col_name in cat_cols:
        # Create markdown cell with column name as heading
        markdown_content = f"### {col_name}"
        markdown_cell = new_markdown_cell(markdown_content)
        cells.append(markdown_cell)
        
        # Create code cell with analysis code
        code_content = f'''col = '{col_name}'

univariate_ordinal_analysis(df[col], f"{{col}} Data")'''
        code_cell = new_code_cell(code_content)
        cells.append(code_cell)



    # Add cells to notebook
    nb.cells = cells
    
    # Write notebook to file
    with open(output_filename, 'w') as f:
        nbformat.write(nb, f)
    
    print(f"Notebook '{output_filename}' created successfully!")

# Define your columns
num_cols = ['Driver_ID', 'Age', 'Gender', 'Education_Level',
       'Dateofjoining', 'LastWorkingDate', 'Joining Designation', 'Grade',
       'Total Business Value', 'Quarterly Rating', 'IncomeCAGR', 'IncomeLast',
       'IncomeIncreased', 'GradeIncreased', 'RatingMean', 'RatingTrend',
        'Ratings', 'Churn', 'EmploymentAge']
cat_cols = ['City','RatingTrendCode',]

# Create the notebook
create_analysis_notebook(num_cols, cat_cols, 'univariate_analysis.ipynb')