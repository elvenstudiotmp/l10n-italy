# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: ElvenStudio
#    Copyright 2015 elvenstudio.it
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
##############################################################################

# import logging
from openerp import api, models, _
from openerp.exceptions import except_orm

# _logger = logging.getLogger(__name__)


class FatturaPAAttachmentOut(models.Model):
    _inherit = 'fatturapa.attachment.out'

    @api.model
    def cron_create_and_send_fatturapa_out(self, limit=10):
        invoice_model = self.env['account.invoice']
        invoices = invoice_model.search(
            [
                ('type', 'in', ['out_invoice', 'out_refund']),
                ('fatturapa_attachment_out_id', '=', False),
                ('date_invoice', '>=', '2019-01-01'),
                ('state', 'in', ['open', 'paid']),
                # skip invoice already exported with errors
                ('fatturapa_out_error', '=', False),
            ],
            order='date_invoice ASC, number ASC',
            limit=limit)

        if invoices:
            wizard_model = self.env['wizard.export.fatturapa']
            # dummy wizard
            wizard = wizard_model.create({})

            context = self.env.context.copy()
            context['active_model'] = invoice_model._name

            ir_values_model = self.env['ir.values']
            e_invoices_to_send = self.env['fatturapa.attachment.out']
            for invoice in invoices:
                try:
                    # simulate invoice print to gather default report data
                    report_data = invoice.invoice_print()
                    report_model = report_data['type']
                    report = self.env[report_model].search(
                        [('report_name', '=', report_data['report_name'])])

                    # attach PDF only if a valid report is defined
                    if report:
                        wizard.report_print_menu = ir_values_model.search(
                            [('value', '=', report_model + ',' + str(report.id))])
                        wizard.generate_attach_report(invoice)

                    # clear report_print_menu field to avoid pdf regeneration
                    wizard.report_print_menu = ir_values_model

                    # export XML e-invoice for the current invoice
                    context['active_ids'] = invoice.ids
                    wizard.with_context(context).exportFatturaPA()

                    # filter public administration invoices,
                    # because they need to be signed before send
                    if not invoice.partner_id.is_pa:
                        e_invoices_to_send |= invoice.fatturapa_attachment_out_id

                except Exception as e:
                    if isinstance(e, except_orm):
                        message = e.value
                    elif isinstance(e, Exception):
                        message = e.message
                    else:
                        message = str(e)

                    invoice.fatturapa_out_error = True
                    invoice.message_post(
                        subject=_("Error during E-invoice export"),
                        body=_(message)
                    )

            # Send via PEC all e-invoices generated
            # (public administration excluded)
            e_invoices_to_send.send_via_pec()

        return True
