# -*- coding: utf-8 -*-
# Copyright (C) 2026 by Michael Blickenstorfer; licensed under AGPL-3 or later; see LICENSE file for details.

from urllib.parse import urlparse

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    current_hostname = fields.Char(
        string='Current Hostname',
        compute='_compute_current_hostname',
    )

    navbar_hostname_color_ids = fields.Many2many(
        comodel_name='navbar.hostname.color',
        string='Hostname Colors',
        compute='_compute_navbar_hostname_color_ids',
        inverse='_inverse_navbar_hostname_color_ids',
        readonly=False,
    )

    navbar_default_color = fields.Char(
        string='Default Navbar Color',
        config_parameter='odoo_navbar_hostname_color.default_navbar_hostname_color',
        help='The default color that will be applied to the Odoo NavBar when the user is logged into an Odoo instance with a hostname that is not explicitly configured. Use a valid CSS color value (e.g., #RRGGBB, rgb(), rgba(), hsl(), hsla(), or named colors).'
    )

    @api.depends()
    def _compute_current_hostname(self):
        def _extract_hostname(value):
            value = (value or '').strip()
            if not value:
                return ''
            parsed = (urlparse(value).hostname or '').strip().lower()
            if parsed:
                return parsed
            return value.split('/', 1)[0].split(':', 1)[0].strip().lower()

        hostname = ''

        # In proxied setups, X-Forwarded-Host is often the most accurate public hostname.
        try:
            httprequest = getattr(request, 'httprequest', None)
            if httprequest is not None:
                forwarded_host = (httprequest.headers.get('X-Forwarded-Host') or '').split(',')[0].strip()
                raw_host = forwarded_host or (httprequest.host or '').strip()
                hostname = raw_host.split(':', 1)[0].strip().lower()
        except Exception:
            hostname = ''

        if not hostname:
            context_base_url = (self.env.context.get('base_url') or '').strip()
            if context_base_url:
                hostname = _extract_hostname(context_base_url)

        if not hostname:
            config = self.env['ir.config_parameter'].sudo()
            for param_name in ('web.base.url', 'report.url'):
                base_url = (config.get_param(param_name, '') or '').strip()
                parsed = _extract_hostname(base_url)
                if parsed:
                    hostname = parsed
                    break

        for record in self:
            record.current_hostname = hostname

    @api.depends()
    def _compute_navbar_hostname_color_ids(self):
        all_colors = self.env['navbar.hostname.color'].search([])
        for record in self:
            record.navbar_hostname_color_ids = all_colors

    def _inverse_navbar_hostname_color_ids(self):
        color_model = self.env['navbar.hostname.color']
        existing = color_model.search([])
        for record in self:
            to_unlink = existing - record.navbar_hostname_color_ids
            if to_unlink:
                to_unlink.unlink()

    @api.constrains('navbar_default_color')
    def _check_navbar_default_color(self):
        color_re = self.env['navbar.hostname.color']._SAFE_COLOR_RE
        for record in self:
            color = (record.navbar_default_color or '').strip()
            if color and not color_re.fullmatch(color):
                raise ValidationError(_('Please enter a valid CSS color value.'))
