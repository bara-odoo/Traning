from odoo import models,fields,api,_

class ResPartner(models.Model):
    _inherit='res.partner'

    offer_ids=fields.One2many('estate.property.offer','partner_id')
