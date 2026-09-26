from odoo import models, fields, api
from odoo.exceptions import UserError

class StockSenseOperation(models.Model):
    _name = 'stocksense.operation'
    _description = 'Inventory Operation (Receipt, Delivery, Transfer)'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    operation_type = fields.Selection([
        ('receipt', 'Receipt'),
        ('delivery', 'Delivery Order'),
        ('internal', 'Internal Transfer'),
    ], string='Operation Type', required=True, default='receipt')
    partner_name = fields.Char(string='Partner / Vendor / Customer')
    source_location_id = fields.Char(string='Source Location', default='Vendor / WH Stock')
    dest_location_id = fields.Char(string='Destination Location', default='WH Stock / Customer')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('ready', 'Ready'),
        ('done', 'Done'),
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            prefix = {
                'receipt': 'WH/IN/',
                'delivery': 'WH/OUT/',
                'internal': 'WH/INT/'
            }.get(vals.get('operation_type', 'receipt'), 'WH/OP/')
            count = self.search_count([('operation_type', '=', vals.get('operation_type'))]) + 1
            vals['name'] = f"{prefix}{count:04d}"
        return super(StockSenseOperation, self).create(vals)

    def action_validate(self):
        for record in self:
            if record.status == 'done':
                raise UserError("This operation is already validated.")
            record.status = 'done'