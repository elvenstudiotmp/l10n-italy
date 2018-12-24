# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2014-2015 Agile Business Group
#    (<http://www.agilebg.com>)
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
#

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class WizardRegistroIva(models.TransientModel):
    _name = "wizard.registro.iva"
    _rec_name = "type"

    period_id = fields.Many2one(
        string=_('Period'),
        comodel_name='account.period',
        default=lambda self: self._get_period(),
        help=_('Select period you want retrieve documents from'),
        required=True
    )

    type = fields.Selection([
        ('customer', 'Customer Invoices'),
        ('supplier', 'Supplier Invoices'),
        ('corrispettivi', 'Corrispettivi'),
        ], 'Layout', required=True,
        default='customer'
    )

    tax_registry_id = fields.Many2one('account.tax.registry', 'VAT registry', required=True)

    journal_ids = fields.Many2many(
        'account.journal',
        'registro_iva_journals_rel',
        'journal_id',
        'registro_id',
        string=_('Journals'),
        help=_('Select journals you want retrieve documents from'),
        required=True
    )

    tax_sign = fields.Float(
        string=_('Tax amount sign'),
        default=1.0,
        help=_('Use -1 you have negative tax amounts and you want to print them prositive')
    )

    message = fields.Char(string=_('Message'), size=64, readonly=True)

    only_totals = fields.Boolean(string=_('Prints only totals'))

    fiscal_page_base = fields.Integer(
        string=_('Last printed page'),
        required=True
    )

    @api.model
    def _get_period(self):
        ctx = dict(self._context or {}, account_period_prefer_normal=True)
        period_id = self.env['account.period'].with_context(context=ctx).find()
        return period_id

    @api.onchange('tax_registry_id')
    def on_change_vat_registry(self):
        self.journal_ids = self.tax_registry_id.journal_ids
        self.type = self.tax_registry_id.type
        if self.type:
            if self.type == 'supplier':
                self.tax_sign = -1
            else:
                self.tax_sign = 1

    def print_registro(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context=context)
        move_obj = self.pool['account.move']
        journal_obj = self.pool['account.journal']

        move_ids = []
        move_dict = {}

        for journal_id in wizard.journal_ids.ids:
            move_domain = [
                # ('journal_id', 'in', [j.id for j in wizard.journal_ids]),
                ('journal_id', '=', journal_id),
                ('period_id', '=', wizard.period_id.id),
                ('state', '=', 'posted'),
            ]

            journal_move_ids = move_obj.search(cr, uid, move_domain, order='date, name')
            if journal_move_ids:
                move_dict[journal_id] = journal_move_ids

            move_ids += journal_move_ids

        if not move_ids:
            raise UserError(_('No documents found in the current selection'))

        journal_ids = journal_obj.search(cr, uid, [('id', 'in', wizard.journal_ids.ids)], order='code ASC')

        datas_form = dict()
        datas_form['period_id'] = wizard.period_id.id
        datas_form['journal_ids'] = journal_ids
        datas_form['journal_move_ids'] = move_dict
        datas_form['tax_sign'] = wizard.tax_sign
        datas_form['fiscal_page_base'] = wizard.fiscal_page_base
        datas_form['registry_type'] = wizard.type
        if wizard.tax_registry_id:
            datas_form['tax_registry_name'] = wizard.tax_registry_id.name
        else:
            datas_form['tax_registry_name'] = ''
        datas_form['only_totals'] = wizard.only_totals
        report_name = 'l10n_it_vat_registries.report_registro_iva'
        datas = {
            'ids': move_ids,
            'model': 'account.move',
            'form': datas_form
        }
        return self.pool['report'].get_action(cr, uid, [], report_name, data=datas, context=context)

    @api.onchange('type')
    def on_type_changed(self):
        if self.type:
            if self.type == 'supplier':
                self.tax_sign = -1
            else:
                self.tax_sign = 1
