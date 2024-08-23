{
    # App Information
    'name': 'Real Estate Invoicing',
    'version': '1.1',
    'summary': 'Real Estate Invoicing Module',
    'category': 'Hidden',
    'license': 'LGPL-3',

    # Author
    'author': 'Karan Modasiya',
    'maintainer': 'Karan Modasiya',

    # Dependencies
    'depends': ['account', 'estate'],

    # Views
    'data': [
        'report/estate_property_templates.xml',
    ],

    # Technical
    'installable': True,
    'application': True,
    'auto_install': False
}
