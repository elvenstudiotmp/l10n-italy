# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
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
##############################################################################

from openerp.osv import fields, orm


class AccountTax(orm.Model):
    _inherit = 'account.tax'
    _columns = {
        'non_taxable_nature': fields.selection([
            ('N1', 'escluse ex art. 15'),
            ('N2', 'non soggette'),
            ('N3', 'non imponibili'),
            ('N4', 'esenti'),
            ('N5', 'regime del margine/IVA non esposta'),
            ('N6', 'inversione contabile (acq. in reverse charge)'),
            ('N7', 'IVA assolta in altro stato UE'),
            ('FC', 'FC applicazione IVA'),
            ], string="Non taxable nature"),
    }
