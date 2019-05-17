# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2012 Domsense s.r.l. (<http://www.domsense.com>).
#    Copyright (C) 2012-15 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012-15 LinkIt Spa (<http://http://www.linkgroup.it>)
#    Copyright (C) 2015 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#


{
    "name": "Period End VAT Statement",
    "version": "8.0.4.0.1",
    'category': 'Generic Modules/Accounting',
    'license': 'AGPL-3',
    "depends": [
        "report",
        "account_voucher",
        "l10n_it_account",
        "l10n_it_vat_registries",
        "l10n_it_fiscalcode",
        "account_invoice_entry_date",
        "l10n_it_fatturapa"
        ],
    "author": "Agile Business Group, Odoo Community Association (OCA)"
              ", LinkIt Spa",
    'website': 'http://www.agilebg.com',
    'data': [
        'wizard/add_period.xml',
        'wizard/remove_period.xml',
        'wizard/wizard_change_vat_period_view.xml',
        'wizard/vat_settlement.xml',
        'statement_workflow.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'report/account_vat_period_end_statement_paperformat.xml',
        'reports.xml',
        'views/report_vatperiodendstatement.xml',
        'views/config.xml',
        'views/account_view.xml',
        'views/account_invoice_view.xml',
        'views/account_move_view.xml',
        'views/account_move_line_view.xml',
    ],
    'external_dependencies': {
        'python': ['pyxb'],
    },
    'installable': True,
}
