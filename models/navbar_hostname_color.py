# -*- coding: utf-8 -*-
# Copyright (C) 2026 by Michael Blickenstorfer; licensed under AGPL-3 or later; see LICENSE file for details.

import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class NavbarHostnameColor(models.Model):
    _name = 'navbar.hostname.color'
    _description = 'Navbar Hostname Color'
    _order = 'hostname'

    _sql_constraints = [
        ('navbar_hostname_color_hostname_uniq', 'unique(hostname)', 'Hostname must be unique.'),
    ]

    _SAFE_COLOR_RE = re.compile(r'^[#(),.%\-a-zA-Z0-9\s]{1,64}$')

    hostname = fields.Char(string='Hostname', required=True, help='The hostname for which this color will be applied to the Odoo NavBar.')
    color = fields.Char(string='Color', required=True, help='The color that will be applied to the Odoo NavBar when the user is logged into an Odoo instance with the specified hostname. Use a valid CSS color value (e.g., #RRGGBB, rgb(), rgba(), hsl(), hsla(), or named colors).')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('hostname'):
                vals['hostname'] = vals['hostname'].strip().lower()
            if vals.get('color'):
                vals['color'] = vals['color'].strip()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('hostname'):
            vals['hostname'] = vals['hostname'].strip().lower()
        if vals.get('color'):
            vals['color'] = vals['color'].strip()
        return super().write(vals)

    @api.constrains('hostname')
    def _check_hostname(self):
        for record in self:
            hostname = (record.hostname or '').strip()
            if not hostname:
                raise ValidationError(_('Hostname cannot be empty.'))
            if ' ' in hostname:
                raise ValidationError(_('Hostname cannot contain spaces.'))

    @api.constrains('color')
    def _check_color(self):
        for record in self:
            color = (record.color or '').strip()
            if not color or not self._SAFE_COLOR_RE.fullmatch(color):
                raise ValidationError(_('Please enter a valid CSS color value.'))
