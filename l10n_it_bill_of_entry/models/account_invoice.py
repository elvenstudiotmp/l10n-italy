# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2013
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
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

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    customs_doc_type = fields.Selection(
        selection=[
            ('bill_of_entry', _('Bill of Entry')),          # bolla
            ('supplier_invoice', _('Supplier Invoice')),    # fornitore
            ('forwarder_invoice', _('Forwarder Invoice')),  # spedizioniere
        ],
        string=_('Customs Doc Type'),
        readonly=True
    )

    supplier_invoice_ids = fields.One2many(
        comodel_name='account.invoice',
        string=_('Supplier Invoices'),
        compute='_get_supplier_invoice_ids'
    )

    forwarder_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string=_('Forwarder Invoice')
    )

    forwarder_bill_of_entry_ids = fields.One2many(
        comodel_name='account.invoice',
        inverse_name='forwarder_invoice_id',
        string=_('Forward Bill of Entries'),
        readonly=True
    )

    forwarder_invoice_ids = fields.One2many(
        comodel_name='account.invoice',
        compute='_get_forwarder_invoice_ids',
        string=_('Forwarder Invoices')
    )

    bill_of_entry_storno_id = fields.Many2one(
        comodel_name='account.move',
        string=_('Bill of Entry Storno'),
        readonly=True
    )

    @api.one
    def _get_forwarder_invoice_ids(self):
        invoice_line_cls = self.env['account.invoice.line']
        if not isinstance(self.id, models.NewId):
            domain = [('forwarded_supplier_invoice_ids', 'in', [self.id])]
            invoice_lines = invoice_line_cls.search(domain)
            if invoice_lines:
                self.forwarder_invoice_ids = invoice_lines.mapped('invoice_id')

    @api.one
    def _get_supplier_invoice_ids(self):
        if self.forwarder_invoice_id and self.forwarder_invoice_id.invoice_line:
            self.supplier_invoice_ids = self.forwarder_invoice_id.invoice_line.mapped('forwarded_supplier_invoice_ids')

    @api.multi
    def action_move_create(self):
        period_obj = self.env['account.period']
        move_obj = self.env['account.move']
        move_line_obj = self.env['account.move.line']

        res = super(AccountInvoice, self).action_move_create()

        for invoice in self:
            if invoice.customs_doc_type == 'forwarder_invoice':

                if not invoice.forwarder_bill_of_entry_ids:
                    raise ValidationError(_(
                        'No Bill of entry defined for this invoice. '
                        'Generate a new one'
                    ))

                for bill_of_entry in invoice.forwarder_bill_of_entry_ids:
                    if bill_of_entry.state not in ('open', 'paid'):
                        raise ValidationError(
                            _(
                                'Cannot validate this invoice, the Bill of '
                                'entry %s must be in open or paid state '
                                '(current state %s)'
                            ) % (bill_of_entry.partner_id.name, bill_of_entry.state)
                        )

                advance_customs_vat_line = False
                for line in invoice.invoice_line:
                    if line.advance_customs_vat or line.forwarded_supplier_invoice_ids:
                            advance_customs_vat_line = True
                            break
                if not advance_customs_vat_line:
                    raise ValidationError(_(
                        'Forwarder invoice %s does not have lines '
                        'with \'Adavance Customs Vat\''
                    ) % invoice.number)

                if not invoice.company_id.bill_of_entry_journal_id:
                    raise ValidationError(_(
                        'No Bill of entry Storno journal configured'
                    ))

                period_ids = period_obj.find(dt=invoice.date_invoice)

                move_vals = {
                    'period_id': period_ids and period_ids[0].id or False,
                    'journal_id': invoice.company_id.bill_of_entry_journal_id.id,
                    'date': invoice.date_invoice,
                    }
                move_lines = []
                for inv_line in invoice.invoice_line:
                    if inv_line.advance_customs_vat or inv_line.forwarded_supplier_invoice_ids:
                        move_line_vals = {
                            'name': _('Customs expenses'),
                            'account_id': inv_line.account_id.id,
                            'debit': 0.0,
                            'credit': inv_line.price_subtotal,
                        }

                        move_lines.append((0, 0, move_line_vals))

                for bill_of_entry in invoice.forwarder_bill_of_entry_ids:
                    move_line_vals = {
                        'name': _("Customs supplier"),
                        'account_id': bill_of_entry.account_id.id,
                        'debit': bill_of_entry.amount_total,
                        'credit': 0.0,
                        'partner_id': bill_of_entry.partner_id.id,
                    }
                    move_lines.append((0, 0, move_line_vals))

                    for boe_line in bill_of_entry.invoice_line:
                        if boe_line.product_id and boe_line.product_id.is_bill_of_entry_tax:
                            continue

                        if boe_line.invoice_line_tax_id:
                            if len(boe_line.invoice_line_tax_id) > 1:
                                raise ValidationError(_(
                                    "Can't handle more than 1 tax for line %s"
                                ) % boe_line.name)

                        line_vals = {
                            'name': _('Extra CEE expenses'),
                            'account_id': boe_line.account_id.id,
                            'debit': 0.0,
                            'credit': boe_line.price_subtotal,
                            }

                        move_lines.append((0, 0, line_vals))
                move_vals['line_id'] = move_lines
                move = move_obj.create(move_vals)

                # check if the move has an invalid storno amount
                if not all([line.state == 'valid' for line in move.line_id]):
                    raise ValidationError(_(
                        'There must be an error into the forwarder invoice '
                        'amount or in the bill of entry invoice amount. '
                        'Please check before validation.'
                    ))
                
                invoice.write({'bill_of_entry_storno_id': move.id})

                reconcile_ids = move_line_obj
                for move_line in move.line_id:
                    for bill_of_entry in invoice.forwarder_bill_of_entry_ids:
                        if move_line.account_id.id == bill_of_entry.account_id.id:
                            reconcile_ids |= move_line
                            for boe_move_line in bill_of_entry.move_id.line_id:
                                if boe_move_line.account_id.id == bill_of_entry.account_id.id:
                                    reconcile_ids |= boe_move_line

                if reconcile_ids:
                    reconcile_ids.reconcile_partial(type='auto')

        return res
        
    @api.multi
    def action_cancel(self):
        res = super(AccountInvoice, self).action_cancel()

        for invoice in self:
            if invoice.bill_of_entry_storno_id:
                bill_of_entry_storno = invoice.bill_of_entry_storno_id
                bill_of_entry_storno.line_id.mapped('reconcile_id').unlink()
                bill_of_entry_storno.button_cancel()
                bill_of_entry_storno.unlink()

        return res
