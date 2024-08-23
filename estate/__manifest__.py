{
    # App Information
    'name': 'Real Estate',
    'version': '3.0',
    'summary': 'Real Estate Module',
    'category': 'Real Estate/Brokerage',
    'license': 'LGPL-3',

    # Author
    'author': 'Karan Modasiya',
    'maintainer': 'Karan Modasiya',

    # Dependencies
    'depends': ['base'],

    # Views and Data
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',

        'report/estate_property_templates.xml',
        'report/ir_action_reports.xml',

        'data/estate.property.type.csv',
    ],
    'demo': [
        'demo/demo_data.xml'
    ],

    # Technical
    'installable': True,
    'application': True,
    'auto_install': False
}
