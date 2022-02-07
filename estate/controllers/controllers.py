# -*- coding: utf-8 -*-
from odoo import http
from odoo .http import request
from odoo.addons.portal.controllers import portal



class MyController(portal.CustomerPortal):

    # # simple hello world
    # @http.route('/estate/index',auth='public')
    # def index(self,**kw):
    #     return "Hello World"

    # # add some data
    # @http.route('/estate/index',auth='public')
    # def index(self,**kw):
    #     return http.request.render('estate.index',{
    #         'data':['bansi','bhumi','jasvi']
    #     })


    # Add property
    @http.route('/estate/property',auth='user' ,website=True)
    def index(self,**kw):
        estate=http.request.env['estate.property']
        return http.request.render('estate.index',{
            'properties':estate.search([])
        })

    
    def _prepare_home_portal_values(self,counters):
        values = super()._prepare_home_portal_values(counters)
        properties = request.env['estate.property']
        values['total_properties'] = properties.search_count([]) or 0
        return values

    @http.route('/my/properties', auth='user', website=True)
    def my_properties(self, **kw):
        estate = request.env['estate.property'].search([])
        values = self._prepare_portal_layout_values()
        values.update({
           'properties':estate, 
        })

        return http.request.render('estate.portal_my_properties',values)
