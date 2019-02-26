# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018 ElvenStudio S.n.c. (<http://www.elvenstudio.it>)
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
##############################################################################
{
    'name': 'Italian Localization - Account Partner Type',
    'version': '8.0.1.0.0',
    'category': 'Hidden',
    'author': "Elven Studio s.n.c.",
    'website': 'http://www.elvenstudio.it',
    'license': 'AGPL-3',
    "depends": [
        'l10n_it_account',
        # 'l10n_it_fiscalcode',  # already satisfied by l10n_it_account
        'l10n_it_ipa',
        'partner_firstname',
    ],

    "data": [
        'views/res_partner_view.xml',
        'views/account_invoice_view.xml',
    ],

    'installable': True,
    # this post_init script only works when you install account and
    # l10n_it_account_partner_type in 2 different instants
    'post_init_hook': 'post_init_hook',
}
