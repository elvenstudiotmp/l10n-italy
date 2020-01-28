# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2011-2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2015 Link It Spa
#    (<http://www.linkgroup.it/>)
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
#
{
    'name': 'Italian Localization - Account Central Journal',
    'version': '8.0.2.1.0',
    'category': 'Localization/Italy',
    'author': 'Link It Spa, Odoo Community Association (OCA)',
    'website': 'http://www.linkgroup.it',
    'license': 'AGPL-3',

    "depends": [
        'account',
        'l10n_it_account'
    ],

    "data": [
        'report/paper.xml',
        'report/central_journal_report.xml',

        'wizard/print_central_journal.xml',

        'views/account_journal_view.xml'
    ],
    "installable": True,
}
