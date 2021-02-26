# -*- coding: utf-8 -*-
import uuid
from odoo import api, fields, models, _


# class HubResUsers(models.Model):
#     _inherit = "res.users"
#
#     uid = fields.Char(string="UUID")
#
#     @api.model
#     def create(self, vals):
#         vals['uid'] = str(uuid.uuid4())
#         return super(HubResUsers, self).create(vals)
