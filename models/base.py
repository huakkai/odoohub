from odoo import fields, models, _


class Base(models.AbstractModel):
    _name = 'odoohub.base'

    name = fields.Char(string='Name')
    state = fields.Selection([('normal', 'Normal'), ('forbid', 'Forbid')], default='normal', string='State')
