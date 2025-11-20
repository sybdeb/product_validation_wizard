{
    'name': 'Product Validation Wizard',
    'version': '18.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Wizard to validate products for publication',
    'description': """
        Een wizard die controleert of producten klaar zijn voor publicatie:
        - Foto aanwezig
        - Prijs > 0
        - Leveranciersvoorraad >= X (via supplier_pricelist_sync)
        - Voldoet aan verkoopcriteria
    """,
    'author': 'sybdeb',
    'website': 'https://github.com/sybdeb/product_validation_wizard',
    'depends': ['product', 'purchase', 'stock', 'website', 'supplier_pricelist_sync'],
    'data': [
        'views/product_views.xml',
        'views/wizard_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
