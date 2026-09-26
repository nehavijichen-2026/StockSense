{
    'name': 'StockSense',
    'version': '1.0',
    'summary': 'Modular Inventory Management System',
    'category': 'Inventory/Warehouse',
    'depends': ['base', 'web'],
    'data': [
        'views/product_views.xml',
        'views/dashboard_views.xml',
        'views/menu_views.xml',
        'views/operation_views.xml',
    ],
    'installable': True,
    'application': True,
}