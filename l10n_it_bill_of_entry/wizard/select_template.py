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

from openerp import models, api, _


class WizardSelectInvoiceTemplate(models.TransientModel):
    _inherit = 'wizard.select.invoice.template'

    @api.multi
    def load_template(self):
        res = super(WizardSelectInvoiceTemplate, self).load_template()
        invoice_cls = self.env['account.invoice']
        if self.env.context.get('active_model') == 'account.invoice':
            invoice = invoice_cls.browse(self.env.context.get('active_id'))

            if invoice and invoice.customs_doc_type == 'forwarder_invoice':
                invoice_id = res['res_id']
                invoice_cls.browse(invoice_id).write({
                    'customs_doc_type': 'bill_of_entry',
                    'forwarder_invoice_id': invoice.id,
                    'journal_id': invoice.journal_id.id
                })

        return res
