# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017    SHS-AV s.r.l. <https://www.zeroincombenze.it>
#    Copyright (C) 2017    Didotech srl <http://www.didotech.com>
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
{
    "name": "Comunicazione periodica IVA",
    "version": "8.0.0.1.7",
    'category': 'Generic Modules/Accounting',
    'license': 'AGPL-3',
    "depends": [
        'l10n_it_ipa',
        'l10n_it_account',
        'l10n_it_fiscalcode',
        'account_invoice_entry_date',
        'l10n_it_vat_registries',
    ],
    "author":  "SHS-AV s.r.l.,"
               " Odoo Italia Associazione",
    'website': 'https://odoo-italia.org',
    'data': [
        'views/add_period.xml',
        'views/remove_period.xml',
        'views/account_view.xml',
        'views/account_invoice_view.xml',
        'views/account_tax_view.xml',
        'views/account_journal.xml',
        # 'views/wizard_export_view.xml',
        'security/ir.model.access.csv',
        'communication_workflow.xml',
    ],
    'external_dependencies': {
        'python': ['pyxb', 'unidecode'],
    },
    'installable': True,
}
