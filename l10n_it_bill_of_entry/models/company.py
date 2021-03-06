# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2013
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#    Copyright (C) 2017 ElvenStudio S.N.C.
#    (<http://www.elvenstudio.it>)
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

from openerp import models, fields, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    bill_of_entry_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string=_('Bill of entry Storno journal'),
        help=_('Journal used for reconciliation of customs supplier')
    )
    

class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    bill_of_entry_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string=_('Bill of entry Storno journal'),
        related='company_id.bill_of_entry_journal_id',
        help=_('Journal used for reconciliation of customs supplier')
    )
