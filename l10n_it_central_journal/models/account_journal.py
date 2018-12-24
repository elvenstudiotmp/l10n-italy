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


class AccountJournal(models.Model):
    _inherit = "account.journal"

    central_journal_exclude = fields.Boolean(
        string=_('Exclude from Central Journal')
    )
