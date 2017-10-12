# -*- coding: utf-8 -*-
##############################################################################
#
# This module is developed by Portcities Indonesia
# Copyright (C) 2017 Portcities Indonesia (<http://portcities.net>).
# All Rights Reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo.exceptions import UserError
from odoo import fields, api, models, _

class LoanOrder(models.Model):
	_name = "loan.order"

	name = fields.Char(string='LO Number', default='New', store=True, required=True)
	partner_id = fields.Many2one('res.partner', 'Customer Name')
	order_date = fields.Datetime(string='Loan Date')
	starting_date = fields.Date(string='Starting Date')
	end_date = fields.Date(string='Ending Date')
	status = fields.Selection(selection='_get_status_selection', string='Status')
	loan_order_ids = fields.One2many('loan.order.line', 'loan_order_id')

	def _get_status_selection(self):
		return (('draft', 'Draft Loan'), ('confirm', 'Loan Sent'), 
			('partially_delivered', 'Partially Delivered'), ('delivered', 'Delivered'), 
			('partially_returned', 'Rartially Returned'), ('returned', 'Returned'))

	def action_confirm(self):
		for loan in self:
			for item in loan.loan_order_ids:
				for product in item.product_id:
					product.qty_available -= item.qty
					product.write({'qty_available': product.qty_available})
					
					# item.free_stock -= item.qty
			# loan.status = 'confirm'
		return True

	def _set_status(self, value):
		for res in self:
			res.status = value
		return True

	@api.model
	def create(self, vals):
		# print vals['status']
		if not vals['status']:
			vals['status'] = 'draft'
			print vals['status']

		if vals.get('name', 'New') == 'New':
			vals['name'] = self.env['ir.sequence'].next_by_code('loan.order')
			print vals['name']

		return super(LoanOrder, self).create(vals)

	def action_partially_delivered(self):
		return self._set_status('partially_delivered')

	def action_delivered(self):
		return self._set_status('delivered')

	def action_partially_returned(self):
		return self._set_status('partially_returned')

	def action_returned(self):
		return self._set_status('returned')


class LoanOrderLine(models.Model):
	_name = "loan.order.line"

	product_id = fields.Many2one('product.product', 'Product')
	name = fields.Text('Description')
	qty = fields.Float('Quantity')
	free_stock = fields.Float()
	loan_order_id = fields.Many2one('loan.order')

	@api.multi
	@api.onchange('product_id')
	def product_id_change(self):
		if not self.product_id:
			return {'domain': {'product_uom': []}}
		
		vals = {}
		product = self.product_id

		title = False
		message = False
		warning = {}
		if product.qty_available <= 0:
			title = _("Warning for %s") % product.name
			message = 'Product currently unavailable'
			warning['title'] = title
			warning['message'] = message
			self.product_id = False
			return {'warning': warning}

		name = product.name_get()[0][1]
		if product.description_sale:
			name += '\n' + product.description_sale

		free_stock = 0
		if product.qty_available:
			free_stock = product.qty_available

		vals['name'] = name
		vals['free_stock'] = free_stock

		title = False
		message = False
		warning = {}
		if product.sale_line_warn != 'no-message':
			title = _("Warning for %s") % product.name
			message = product.sale_line_warn_msg
			warning['title'] = title
			warning['message'] = message
			if product.sale_line_warn == 'block':
				self.product_id = False
			return {'warning': warning}

		self.update(vals)

	@api.model
	def create(self, vals):
		print 'create order line'
		
		return super(LoanOrderLine, self).create(vals)

	@api.multi
	def write(self, vals):
		print 'write order line'
		
		return super(LoanOrderLine, self).write(vals)