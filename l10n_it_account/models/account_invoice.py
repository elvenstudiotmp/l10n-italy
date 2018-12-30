# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018 ElvenStudio S.n.c. (<http://www.elvenstudio.it>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

from openerp import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _refund_cleanup_lines(self, lines):
        refund_lines = super(AccountInvoice, self)._refund_cleanup_lines(lines)

        account_cls = self.env['account.account']
        # override account_id if a refund account is defined
        invoice_lines = []
        for line in refund_lines:
            if isinstance(line[2], dict):
                account_id = line[2].get('account_id', False)
                if account_id:
                    account = account_cls.browse(account_id)
                    if account and account.refund_invoice_account_id:
                        line[2]['account_id'] = account.refund_invoice_account_id.id

            invoice_lines.append(line)

        return invoice_lines
