# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2018 Elven Studio (<http://www.elvenstudio.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection(
        string=_('Partner Type'),
        selection=[
            ('contact', _('Generic Contact')),
            ('company', _('Company')),
            ('individual', _('Individual Company')),
            ('non-profit', _('Non Profit Organization')),
            ('public', _('Public Administration')),
            ('person', _('Person')),
        ],
        default='contact',
        required=False,
        help=_(
            'Choose the partner type due to your needed, '
            'in order to fill the right fields.\n'
            ' - Generic Contact: generic partner without any fiscal information.\n'
            ' - Company: Company contact, use this when registering a new company.\n'
            ' - Individual Company: A company that has fiscal information related to a person.\n'
            ' - Public administration: A company that has fiscal information related to a public organization.\n'
            ' - Person: A private citizen contact, used in sale or purchase invoices.'
        )
    )

    @api.one
    @api.onchange('partner_type')
    def onchange_partner_type(self):
        if self.partner_type == 'company':
            self.is_company = True
            self.vat_subjected = True
            self.individual = False
            self.is_pa = False
        elif self.partner_type == 'individual':
            self.is_company = True
            self.vat_subjected = True
            self.individual = True
            self.is_pa = False
        elif self.partner_type == 'person':
            self.is_company = False
            self.vat_subjected = False
            self.individual = True
            self.is_pa = False
        elif self.partner_type == 'public':
            self.is_company = True
            self.vat_subjected = False
            self.individual = False
            self.is_pa = True
        elif self.partner_type == 'contact':
            self.is_company = False
            self.vat_subjected = False
            self.individual = False
            self.is_pa = False
        elif self.partner_type == 'non-profit':
            self.is_company = True
            self.vat_subjected = False
            self.individual = False
            self.is_pa = False

