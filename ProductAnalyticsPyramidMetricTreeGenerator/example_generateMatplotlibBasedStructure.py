from kpi_tree_generator import KPITreeGenerator, create_example_diagram

# Use the built-in example
fig = create_example_diagram()

# Or create your own
kpi_data = {
    'top_kpi': {
        'name': 'GROWTH',
        'description': 'Monthly Active Users (MAU)'
    },
    'categories': [
        {
            'name': 'ACQUISITION',
            'team': 'Marketing',
            'metric': 'New user signups',
            'subcategories': [
                {'name': 'Organic', 'type': 'normal'},
                {'name': 'Paid', 'type': 'normal'},
                {'name': 'Referral', 'type': 'action'}
            ]
        },
        {
            'name': 'ACTIVATION',
            'team': 'Product',
            'metric': 'Day 1 retention rate',
            'subcategories': [
                {'name': 'Onboarding completion', 'type': 'action'}
            ]
        }
    ]
}

#generator = KPITreeGenerator()
#fig = generator.generate_kpi_tree(kpi_data)
fig.savefig('my_kpi_tree.png', dpi=300, bbox_inches='tight')