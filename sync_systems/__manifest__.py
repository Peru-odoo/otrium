# -*- coding: utf-8 -*-
{
    'name': "Synchronize Systems",

    'summary': """
        The goal of this module is to create an interface with a purpose to synchronize two systems.""",


    'author': "Eslam Tharwat",
    'website': "eslam.tharwaat@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'tools',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['base','base_setup'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/content_ir_cron.xml',
        'views/view.xml',
        'data/device_ir_cron.xml',
        'views/device_b.xml',
        'views/content_b.xml',
        'views/res_config_settings.xml',
    ],

}
