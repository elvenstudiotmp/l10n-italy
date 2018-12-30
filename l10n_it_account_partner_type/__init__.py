# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018 ElvenStudio S.n.c. (<http://www.elvenstudio.it>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from . import models

import logging
from openerp import SUPERUSER_ID


def post_init_hook(cr, registry):
    _logger = logging.getLogger('openerp.addons.l10n_it_account_partner_type')

    res_partner_model = registry['res.partner']
    _logger.info('Setting values for res.partner new field: Partner Type')
    # By default, all partners will be set to contact

    _logger.info('Setting partners of type person')
    # Case a: person
    # type is person -> fiscalcode not is empty and
    #                   vat is empty and
    #                   parent_id is false and
    #                   is_pa is false
    #
    # All persons have a fiscalcode set and
    # they are not a company or public administration and
    # the field vat must be empty

    # add parent_id condition in order to exclude sub account
    partner_person_domain = [
        ('fiscalcode', '!=', False),
        ('vat', '=', False),
        ('parent_id', '=', False),
        ('is_pa', '=', False)
    ]
    partner_person_vals = {
        'partner_type': 'person',
        'vat_subjected': False,
        'individual': True,
        'is_company': False
    }
    partner_person_ids = res_partner_model.search(cr, SUPERUSER_ID, partner_person_domain)
    res_partner_model.write(cr, SUPERUSER_ID, partner_person_ids, partner_person_vals)
    _logger.info('Partners of type person correctly sets')

    _logger.info('Setting partners of type individual')
    # Case b: individual
    # type is individual -> fiscalcode length equal to 16 and
    #                       vat is not empty and
    #                       vat is not equal to fiscalcode and
    #                       parent_id is set
    #
    # Individual companies are company related to a single person,
    # so we need to have the company vat number and the person fiscalcode.
    partner_individual_domain = [
        ('fiscalcode', '!=', False),
        ('vat', '!=', False),
        ('parent_id', '=', False)
    ]
    partner_individual_vals = {
        'partner_type': 'individual',
        'vat_subjected': True,
        'individual': True,
        'is_company': True
    }
    partner_individual_ids = res_partner_model.search(cr, SUPERUSER_ID, partner_individual_domain)
    partner_individuals = res_partner_model.browse(cr, SUPERUSER_ID, partner_individual_ids)
    partner_individual_to_update_ids = []
    for partner in partner_individuals:
        if partner.vat != partner.fiscalcode and len(partner.fiscalcode) == 16:
            partner_individual_to_update_ids.append(partner.id)

    res_partner_model.write(cr, SUPERUSER_ID, partner_individual_to_update_ids, partner_individual_vals)
    _logger.info('Partners of type individual correctly sets')

    _logger.info('Setting partners of type company')
    # Case c: company
    # type is company -> fiscalcode is not set or equal to vat and
    #                    vat is not empty and
    #                    parent_id is not set and
    #                    is_pa is false
    #
    # Italian companies can have the fiscalcode equal to vat without
    # the country suffix (eg. vat: IT0123456789 -> fiscalcode 0123456789).
    partner_company_domain = [
        ('vat', '!=', False),
        ('parent_id', '=', False),
        ('is_pa', '=', False),
    ]
    partner_company_vals = {
        'partner_type': 'company',
        'vat_subjected': True,
        'is_company': True,
        'individual': False
    }
    partner_company_ids = res_partner_model.search(cr, SUPERUSER_ID, partner_company_domain)
    partner_companies = res_partner_model.browse(cr, SUPERUSER_ID, partner_company_ids)
    partner_company_to_update_ids = []
    for partner in partner_companies:
        if partner.vat == partner.fiscalcode or \
           partner.fiscalcode in partner.vat or \
           not partner.fiscalcode:
            partner_company_to_update_ids.append(partner.id)

    res_partner_model.write(cr, SUPERUSER_ID, partner_company_to_update_ids, partner_company_vals)
    _logger.info('Partners of type company correctly sets')

    _logger.info('Setting partners of type public administration')
    # Case d: public administration
    # type is company -> fiscalcode is set and
    #                    parent_id is not set and
    #                    is_pa is True or ipa_code is set
    #
    # Some italian public administration does not have vat, but only fiscalcode
    # must be always available. In addition, contact can have the ipa code set
    # but is_pa field sets to false to l10n_it_ipa module.
    partner_public_domain = [
        ('fiscalcode', '!=', False),
        ('parent_id', '=', False),
        '|',
        ('is_pa', '=', True),
        ('ipa_code', '=', True),
    ]
    partner_public_vals = {
        'partner_type': 'public',
        'vat_subjected': False,
        'is_company': True,
        'individual': False,
        'is_pa': True,
    }
    partner_public_ids = res_partner_model.search(cr, SUPERUSER_ID, partner_public_domain)
    res_partner_model.write(cr, SUPERUSER_ID, partner_public_ids, partner_public_vals)
    _logger.info('Partners of type public administration correctly sets')

    _logger.info('Fields setup completed')
