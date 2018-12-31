# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Alessandro Camilli (a.camilli@openforce.it)
#    Copyright (C) 2015
#    Apulia Software srl - info@apuliasoftware.it - www.apuliasoftware.it
#    Openforce di Camilli Alessandro - www.openforce.it
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

    of_account_end_vat_statement_interest = fields.Boolean(
        string=_('Interest on End Vat Statement'),
        help=_('Apply interest on end vat statement')
    )

    of_account_end_vat_statement_interest_percent = fields.Float(
        string=_('Interest on End Vat Statement - %'),
        help=_('Apply interest on end vat statement')
    )

    of_account_end_vat_statement_interest_account_id = fields.Many2one(
        comodel_name='account.account',
        string=_('Interest on End Vat Statement - Account'),
        help=_('Apply interest on end vat statement')
    )

    of_account_end_vat_statement_tax_authority = fields.Many2one(
        comodel_name='res.partner',
        string=_('Tax Autority on End Vat Statement'),
        help=_('Set the default tax autority to use '
               'into the end vat statement.')
    )

    of_account_end_vat_statement_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string=_('End Vat Statement Journal'),
        help=_('Set the default account journal to use '
               'into the end vat statement.')
    )

    of_account_end_vat_statement_credit_account_id = fields.Many2one(
        comodel_name='account.account',
        string=_('End Vat Statement Credit Account'),
        help=_('Set the default account when the end vat statement total '
               'is less than zero.')
    )

    of_account_end_vat_statement_debit_account_id = fields.Many2one(
        comodel_name='account.account',
        string=_('End Vat Statement Debit Account'),
        help=_('Set the default account when the end vat statement total '
               'is greater than zero.')
    )
