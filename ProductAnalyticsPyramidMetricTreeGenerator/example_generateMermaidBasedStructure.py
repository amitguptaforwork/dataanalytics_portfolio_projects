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

saas_kpis = {
    'top_kpi': {
        'name': 'ARR GROWTH',
        'description': 'Annual Recurring Revenue'
    },
    'categories': [
        {
            'name': 'NEW BUSINESS',
            'team': 'Sales',
            'metric': 'New customer ARR',
            'subcategories': [
                {'name': 'Enterprise', 'type': 'normal'},
                {'name': 'SMB', 'type': 'normal'}
            ]
        },
        {
            'name': 'EXPANSION',
            'team': 'Customer Success',
            'metric': 'Expansion rate %',
            'subcategories': [
                {'name': 'Upsells', 'type': 'action'},
                {'name': 'Cross-sells', 'type': 'action'}
            ]
        },
        {
            'name': 'RETENTION',
            'team': 'Product',
            'metric': 'Net revenue retention',
            'subcategories': [
                {'name': 'Churn reduction', 'type': 'action'}
            ]
        }
    ]
}
mermaid_code = generate_mermaid_diagram(saas_kpis)
# Save to file
with open('saas_kpi_tree.mmd', 'w') as f:
    f.write(mermaid_code)




ecommerce_kpis = {
    'top_kpi': {
        'name': 'REVENUE',
        'description': 'Monthly Gross Merchandise Value'
    },
    'categories': [
        {
            'name': 'TRAFFIC',
            'team': 'Marketing',
            'metric': 'Unique visitors',
            'subcategories': [
                {'name': 'SEO', 'type': 'normal'},
                {'name': 'Paid ads', 'type': 'normal'},
                {'name': 'Social', 'type': 'normal'}
            ]
        },
        {
            'name': 'CONVERSION',
            'team': 'Product',
            'metric': 'Conversion rate %',
            'subcategories': [
                {'name': 'Cart abandonment', 'type': 'action'},
                {'name': 'Checkout flow', 'type': 'action'}
            ]
        },
        {
            'name': 'AOV',
            'team': 'Merchandising',
            'metric': 'Average order value',
            'subcategories': [
                {'name': 'Recommendations', 'type': 'action'},
                {'name': 'Bundles', 'type': 'action'}
            ]
        }
    ]
}

mermaid_code = generate_mermaid_diagram(ecommerce_kpis)
# Save to file
with open('ecom_kpi_tree.mmd', 'w') as f:
    f.write(mermaid_code)