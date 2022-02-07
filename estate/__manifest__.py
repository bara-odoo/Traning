# -*- coding: utf-8 -*-
{
    'name': 'Real_Estate',
    'category': 'Sales',
    'application': 'True',
    'version':'1.0',
    'depends':['base','account','website','portal'],
    'data': [
    	'security/ir.model.access.csv',
    	'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'wizard/add_offer_views.xml',
        'security/open_realestate_security.xml',
        'views/estate_index.xml',
        'views/estate_portal_view.xml',
        
    ],
    
}
