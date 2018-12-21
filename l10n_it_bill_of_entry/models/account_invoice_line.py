# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2013
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#    Copyright (C) 2017 ElvenStudio S.N.C.
#    (<http://www.elvenstudio.it>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, _


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # Deprecated, kept for compatibility reason
    advance_customs_vat = fields.Boolean(string=_('Advance Customs Vat'))

    forwarded_supplier_invoice_ids = fields.Many2many(
        comodel_name='account.invoice',
        relation='fsi_invoice_rel',
        column1='invoice_line_id',
        column2='invoice_id',
        string=_('Forwarded Supplier Invoices'),
        domain=[('customs_doc_type', '=', 'supplier_invoice')]
    )

