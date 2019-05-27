# -*- coding: utf-8 -*-

from datetime import datetime
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

vat_statement_submission_day = 16


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    vat_period_id = fields.Many2one(
        string=_('Vat Period'),
        comodel_name='account.period',
        readonly=True,
        states={'draft': [('readonly', False)]},
        copy=False,
        help=_('Define the vat statement period '
               'in witch the invoice will be included.')
    )

    @api.model
    def _get_vat_period_id(self, invoice_date, registration_date):
        period_model = self.env['account.period']
        invoice_period = period_model.find(invoice_date)
        registration_period = period_model.find(registration_date)
        if invoice_period.id == registration_period.id:
            vat_period = invoice_period

        # if the invoice_period is already sent, ignore it
        elif invoice_period.vat_statement_id and invoice_period.vat_statement_id.state != 'draft':
            vat_period = registration_period

        else:
            # if the registration date is over the day of vat submission,
            # we cannot use invoice_period in the new invoice,
            # even if it is not sent.
            registration_date = datetime.strptime(registration_date, DF)
            if registration_date.day < vat_statement_submission_day:
                vat_period = invoice_period
            else:
                vat_period = registration_period

        return vat_period

    @api.one
    @api.onchange('registration_date')
    def onchange_registration_date(self):
        if self.type in ('in_invoice', 'in_refund') and \
           self.registration_date and \
           self.date_invoice:
            self.vat_period_id = self._get_vat_period_id(
                self.date_invoice, self.registration_date)

    @api.one
    @api.constrains('vat_period_id')
    def check_vat_period_id(self):
        if self.vat_period_id:
            # check if vat_period is already used into a vat statement
            if self.vat_period_id.vat_statement_id and \
               self.vat_period_id.vat_statement_id.state != 'draft':
                raise ValidationError(_(
                    'Cannot use this period, because it is already sent!\n'
                    'Statement: %s') % self.vat_period_id.vat_statement_id.name)

            if self.type in ('in_invoice', 'in_refund') and \
               self.registration_date and \
               self.date_invoice:
                # Check if the vat_period specified by the user is correct.
                # User can choose from two period:
                #  - the period that comes from the invoice date;
                #  - the period that comes from the registration date.
                #
                # It will chose one or the other depending of VAT total amount.
                suggested_vat_period = self._get_vat_period_id(self.date_invoice, self.registration_date)
                registration_period = self.env['account.period'].find(self.registration_date)
                # If the user have chosen a vat period different from the suggested,
                # then it must be the registration period.
                if self.vat_period_id.id != suggested_vat_period.id:
                    # If the suggested period is equal to registration period,
                    # then the invoice is registered over the vat submission date,
                    # So the user has selected a wrong period.
                    if suggested_vat_period.id == registration_period.id:
                        raise ValidationError(_(
                            'Cannot use previous vat period when '
                            'registration day is over 15 of the month!'))

                    # If the user have selected a vat period different from
                    # the two correct periods, then raise an exception
                    if self.vat_period_id.id != registration_period.id:
                        raise ValidationError(_('Invalid vat period chosen!'))

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()

        for invoice in self:
            if invoice.type in ('in_invoice', 'in_refund'):
                if invoice.vat_period_id:
                    # if vat_period is already set (and checked by constraint),
                    # just store it in invoice related move and move lines.
                    invoice.move_id.write({'vat_period_id': invoice.vat_period_id.id})
                    invoice.move_id.line_id.write({'vat_period_id': invoice.vat_period_id.id})
                else:
                    # For incoming invoice, use the suggested period.
                    vat_period = self._get_vat_period_id(invoice.date_invoice, invoice.registration_date)
                    # Set it into invoice, move and move lines.
                    # If it is wrong, constraint method will raise exception.
                    invoice.write({'vat_period_id': vat_period.id})
                    invoice.move_id.write({'vat_period_id': vat_period.id})
                    invoice.move_id.line_id.write({'vat_period_id': vat_period.id})
            else:
                # For outgoing invoice, we will use the standard period.
                vat_period_id = invoice.period_id.id
                invoice.write({'vat_period_id': vat_period_id})
                invoice.move_id.write({'vat_period_id': vat_period_id})
                invoice.move_id.line_id.write({'vat_period_id': vat_period_id})

        return res

    @api.multi
    def action_change_vat_period(self, vat_period):
        for invoice in self:
            if invoice.vat_period_id.vat_statement_id and \
               invoice.vat_period_id.vat_statement_id.state != 'draft':
                raise ValidationError(_(
                    'Cannot change vat period for invoice %s: '
                    'this period is already sent!\n'
                    'Statement: %s') % (invoice.name, invoice.vat_period_id.vat_statement_id.name))

        self.write({'vat_period_id': vat_period.id})
        moves = self.mapped('move_id')
        moves.write({'vat_period_id': vat_period.id})
        moves.mapped('line_id').write({'vat_period_id': vat_period.id})
        return True
