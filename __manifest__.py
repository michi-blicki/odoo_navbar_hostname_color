# -*- coding: utf-8 -*-
{
    'name': "Odoo NavBar Hostname Color",

    'summary': "Change the color of the Odoo NavBar based on the hostname",

    'description': """
Configure Hostnames in the settings and assign a color to each hostname. The color will be applied to the 
Odoo NavBar when the user is logged into an Odoo instance with that hostname. This is useful for quickly
identifying which Odoo Instance you are working in, especially when you have multiple instances like
development, quality assurance, project or production.
You can also configure a default color for hostnames, that are not explicitly configured.
    """,

    #
    # Issuer Specification
    'author': "Michael Blickenstorfer",
    'website': "https://www.github.com/michi-blicki/odoo_navbar_hostname_color",
    'license': "AGPL-3",
    
    'category': 'Website',
    'version': '18.0.1.0.0',
    'application': False,
    'auto_install': False,
    'installable': True,

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'web',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/navbar_hostname_color_views.xml',
        'views/res_config_settings_views.xml',
        'views/webclient_templates.xml',
    ],

    'assets': {
        'web.assets_backend': [],
    },

}

