{
    # App Information
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Real Estate Module',
    'category': 'Hidden',
    'license': 'LGPL-3',

    # Author
    'author': 'Karan Modasiya',
    'maintainer': 'Karan Modasiya',

    # Dependencies
    'depends': ['base'],

    # Views
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],

    # Technical
    'installable': True,
    'application': True,
    'auto_install': False
}
