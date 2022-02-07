from odoo import models,fields

class AdmissionProcess(models.Model):
    _name='register.process'
    _description='Register Form'

    name=fields.Text()

