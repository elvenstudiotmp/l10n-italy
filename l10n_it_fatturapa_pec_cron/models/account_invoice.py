# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: ElvenStudio
#    Copyright 2015 elvenstudio.it
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
##############################################################################

from openerp import api, models, fields, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    fatturapa_out_error = fields.Boolean(
        string=_('With issues during last export'),
        help=_('If is set to true, then invoice had issues '
               'during last export via cron'),
        default=False,
        readonly=True
    )

    @api.multi
    def action_fatturapa_out_error_resolved(self):
        self.message_post(
            subject=_('E-invoice errors marked as resolved'),
            body=_('User %s has marked e-invoice errors as resolved') % self.env.user.name
        )
        return self.write({'fatturapa_out_error': False})
