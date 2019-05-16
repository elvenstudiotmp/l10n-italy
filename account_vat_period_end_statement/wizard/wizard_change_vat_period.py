# -*- coding: utf-8 -*-

from openerp import models, fields, api, _


class AccountInvoiceWizardChangeVatPeriod(models.TransientModel):
    _name = 'account.invoice.wizard.change_vat_period'

    invoice_id = fields.Many2one(
        string=_('Invoice'),
        comodel_name='account.invoice',
        default=lambda self: self._get_invoice_id(),
        readonly=True
    )

    vat_period_id = fields.Many2one(
        string=_('Vat Period'),
        comodel_name='account.period',
        required=True
    )

    @api.model
    def _get_invoice_id(self):
        invoice = self.env['account.invoice']
        invoice_id = self.env.context.get('active_id', False)
        if invoice_id:
            invoice = invoice.browse(invoice_id)
        return invoice

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        return self.invoice_id.action_change_vat_period(self.vat_period_id)
