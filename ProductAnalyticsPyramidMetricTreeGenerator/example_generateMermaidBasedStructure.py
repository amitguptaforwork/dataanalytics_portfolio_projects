# Generate Mermaid code
from kpi_tree_generator import generate_mermaid_diagram

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

# Generate Mermaid code
mermaid_code = generate_mermaid_diagram(kpi_data)
print(mermaid_code)

# Save to file
with open('kpi_tree.mmd', 'w') as f:
    f.write(mermaid_code)


    