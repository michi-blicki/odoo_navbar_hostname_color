# -*- coding: utf-8 -*-
# Copyright (C) 2026 by Michael Blickenstorfer; licensed under AGPL-3 or later; see LICENSE file for details.

from odoo import http
from odoo.http import request


class NavbarHostnameColorController(http.Controller):
    @http.route(
        '/odoo_navbar_hostname_color/navbar.css',
        type='http',
        auth='user',
        methods=['GET'],
        csrf=False,
    )
    def navbar_css(self, **kwargs):
        hostname = ((request.httprequest.host or '').split(':', 1)[0]).strip().lower()
        color = self._get_navbar_color_for_hostname(hostname)

        css = ''
        if color:
            css = '.o_main_navbar { background-color: %s !important; }\n.o_menu_sections { background-color: %s !important; }' % (color, color)

        return request.make_response(
            css,
            headers=[
                ('Content-Type', 'text/css; charset=utf-8'),
                ('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0'),
            ],
        )

    @staticmethod
    def _get_navbar_color_for_hostname(hostname):
        hostname_color = request.env['navbar.hostname.color'].sudo().search(
            [('hostname', '=ilike', hostname)],
            limit=1,
        )
        if hostname_color:
            return (hostname_color.color or '').strip()

        return (
            request.env['ir.config_parameter']
            .sudo()
            .get_param('odoo_navbar_hostname_color.default_navbar_hostname_color', '')
            .strip()
        )
