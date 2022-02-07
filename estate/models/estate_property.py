from odoo import models,fields,api
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError ,ValidationError



class EstatePropertyOffer(models.Model):
	_name='estate.property.offer'
	_description='Estate Property Offer'

	name=fields.Text()
	offer_person=fields.Many2one('res.partner')
	price=fields.Float()
	offer_date=fields.Date(default=lambda self:fields.Datetime.now(),copy=False)
	offer_status=fields.Selection([('accept','Accepted'),('reject','Rejected')])
	status=fields.Selection([('accepted','Accepted'),('refuse','Refused')])
	valid_days=fields.Integer(default=7)
	valid_till=fields.Date(compute="_valid_till_date")
	partner_id=fields.Many2one('res.partner')
	property_id=fields.Many2one('estate.property')
	property_type_id=fields.Many2one(related="property_id.property_type_id",store=True)

	@api.depends("offer_date","valid_days")
	def _valid_till_date(self):
		print("\n\n _valid_till_date called")
		for record in self:
			record.valid_till=record.offer_date + datetime.timedelta(days=record.valid_days)

	def action_accepted(self):
		for record in self:
			record.status='accepted'
			# Set buyer and Selling price
			record.property_id.selling_price=record.price
			record.property_id.buyer_id=record.partner_id
            


	def action_refused(self):
		for record in self:
			record.status='refuse'


	     

    

class EstatePropertyTag(models.Model):
	_name ='estate.property.tag'
	_description ='Estate Propert Tage'

	name=fields.Char()
	color=fields.Integer()
	# _sql_constraints=[('unique_property_tag_name','unique(name)', 'Tag Can Not Duplicated']


class EstatePropertyType(models.Model):
	_name ='estate.property.type'
	_description='Estate Property Type'

	name = fields.Char()
	property_ids=fields.One2many('estate.property','property_type_id')
	_order="id desc"
	offer_ids=fields.One2many('estate.property.offer','property_type_id')
	offer_count=fields.Integer(compute="_compute_count_offer")
	
	# _sql_constraints=[('unique_property_type_name', 'unique(name)', 'Type Can Not Duplicated')]
	@api.depends('offer_ids')
	def _compute_count_offer(self):
		for record in self:
			record.offer_count=len(record.offer_ids)

class Real_EstateProperty(models.Model):
	_name = "estate.property"
	_description = "estate_property"
    # _sql_constraints=[('positive_price', 'check(expected_price >= 0)', 'Enter Positive Value')]


	#def test(self):
		#return fields.Datetime.now()

		# and argument in the defult=test

	name =fields.Char(string="Property Name",default="Test",required=True)
	description = fields.Text()
	postcode = fields.Char()
	date_availability = fields.Date(default=lambda self: fields.Datetime.now(),copy=False)
	expected_price =fields.Float(required=True)
	selling_price = fields.Float(copy=False,readonly=True)
	bedrooms =fields.Integer(default=2)
	living_area =fields.Integer()
	facades=fields.Integer()
	garage=fields.Boolean()
	garden=fields.Boolean()
	garden_area=fields.Integer()
	garden_orientation=fields.Selection([
		('North','North'),
		('South','South'),
		('East','East'),
		('West','west')
		])

	active=fields.Boolean(default=True)
	image=fields.Image()
	property_type_id = fields.Many2one('estate.property.type')
	salesman_id=fields.Many2one('res.users')
	buyer_id=fields.Many2one('res.partner')
	property_tag_ids=fields.Many2many('estate.property.tag')
	property_offer_ids=fields.One2many('estate.property.offer','property_id')
	#compute Field
	total_area=fields.Integer(compute="_compute_area" , inverse="_inverse_area")
	best_price=fields.Float(compute="_compute_best_price")
	validity=fields.Integer(default=7)
	date_deadline=fields.Date(compute="_compute_date_deadline")
	state=fields.Selection([('new','New'),('sold','Sold'),('cancel','Canceled')],default='new')
	# currency_id=fields.Many2one('res.currency',default=lambda self: self.env.currency_id)
	

	@api.depends('validity')
	def _compute_date_deadline(self):
		for record in self:
			record.date_deadline= fields.Date.add(record.date_availability,days=record.validity)

	
	@api.depends('garden')
	def _onchange_garden(self):
		for record in self:
			if record.garden:
				record.garden_area=10
				record.garden_orientation='north'
			else:
				record.garden_area=0
				record.garden_orientation=None

	# action Method

	def action_sold(self):
		for record in self:
			if record.state=="cancel":
				raise UserError("Property Can Not Sold")
			record.state="sold"

	def action_cancel(self):
		for record in self:
			if record.state=="sold":
				raise UserError("Property Can Be Not Cancel")
			record.state="cancel"


	@api.depends('property_offer_ids.price')
	def _compute_best_price(self):
		for record in self:
			max_price=0
			for offer in record.property_offer_ids:
				if offer.price > max_price:
					max_price=offer.price
			record.best_price=max_price


	@api.depends('living_area','garden_area')
	def _compute_area(self):
		for record in self:
			record.total_area= record.living_area + record.garden_area
    

	def _inverse_area(self):
		for record in self:
			record.living_area=record.garden_area=record.total_area / 2


	# Constraints Validation Error

    # @api.constrains('living_area', 'garden_area')
    # def _check_garden_area(self):
    #     for record in self:
    #         if record.living_area < record.garden_area:
    #             raise ValidationError("Garden Can Not Biggest Than The Living Area")


	# TASK -1 

class EstatePropertyMyProperty(models.Model):
    _name = 'estate.property.myproperty'
    _description = 'This is the Task Menu'

	#name = fields.Char()
    description = fields.Text()
    property_id = fields.Many2one('estate.property')
    partner_id = fields.Many2one('res.partner')
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')])
    bedrooms = fields.Integer()
    price = fields.Float()
    living_area = fields.Integer()
    name = fields.Char(default="Unknown" , required=True  , string="Name")
    description = fields.Text()
    postcode = fields.Char()
    date_availability =  fields.Date(default=lambda self:fields.Datetime.now() , copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades =  fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West')
        ])
    image = fields.Image()
    total_area = fields.Integer()
    best_price = fields.Float()
    validity = fields.Integer(default=7)
    date_deadline = fields.Date()
    state = fields.Selection([('new','New'),('sold','Sold'),('cancle','Cancle')],default='new')
    salesman_id = fields.Many2one('res.users',default=lambda self:self.env.user)  