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


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.multi
    def product_id_change(
            self, product, uom_id, qty=0, name='', type='out_invoice',
            partner_id=False, fposition_id=False, price_unit=False,
            currency_id=False, company_id=None
    ):
        res = super(AccountInvoiceLine, self).product_id_change(
            product, uom_id, qty=qty,
            name=name, type=type, partner_id=partner_id,
            fposition_id=fposition_id, price_unit=price_unit,
            currency_id=currency_id,  company_id=company_id
        )

        account_cls = self.env['account.account']
        # override account_id if refund invoice
        if type in ('out_refund', 'in_refund'):
            value = res.get('value', False)
            if value and isinstance(value, dict):
                account_id = value.get('account_id', False)
                if account_id:
                    account = account_cls.browse(account_id)
                    if account and account.refund_invoice_account_id:
                        res['value']['account_id'] = account.refund_invoice_account_id.id

        return res

