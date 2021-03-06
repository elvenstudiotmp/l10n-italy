# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018 ElvenStudio S.n.c. (<http://www.elvenstudio.it>)
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

from openerp import models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def _get_invoice_line_vals(self, move, partner, inv_type):
        res = super(StockMove, self)._get_invoice_line_vals(
            move, partner, inv_type)

        if inv_type in ('out_refund', 'in_refund'):
            # override account_id if a refund account is defined
            account_id = res.get('account_id', False)
            if account_id:
                account = self.env['account.account'].browse(account_id)
                if account and account.refund_invoice_account_id:
                    res['account_id'] = account.refund_invoice_account_id.id

        return res
