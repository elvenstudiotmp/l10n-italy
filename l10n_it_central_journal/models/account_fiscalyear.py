# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 ISA s.r.l. (<http://www.isa.it>).
#    Copyright (C) 2015 Link It Spa
#    (<http://www.linkgroup.it/>)
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################

from openerp import models, fields, _
import openerp.addons.decimal_precision as dp


class AccountFiscalYear(models.Model):
    _inherit = "account.fiscalyear"

    date_last_print = fields.Date(
        string=_('Last printed date')
    )

    progressive_page_number = fields.Integer(
        string=_('Progressive of the page'),
        default=0
    )

    progressive_line_number = fields.Integer(
        string=_('Progressive line'),
        default=0
    )

    progressive_credit = fields.Float(
        string=_('Progressive Credit'),
        digits_compute=dp.get_precision('Account'),
        default=lambda *a: float()
    )

    progressive_debit = fields.Float(
        string=_('Progressive Debit'),
        digits_compute=dp.get_precision('Account'),
        default=lambda *a: float()
    )
