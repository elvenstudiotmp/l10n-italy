# -*- coding: utf-8 -*-
# Copyright 2019 Domenico Stragapede - Elven Studio S.N.C.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from openerp import api, SUPERUSER_ID
_log = logging.getLogger(__name__ + ' 8.0.1.2.5')


def migrate(cr, version):
    """Copy number from name for existing fatturapa.attachment.out invoices"""
    if not version:
        return

    _log.info('Upgrading fatturapa.attachment.out number field')

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        domain = [('number', '=', False), ('name', '!=', False)]
        e_trasmissions = env['fatturapa.attachment.out'].search(domain)
        _log.info("Total invoices to update: %d", len(e_trasmissions))
        for e_trasmission in e_trasmissions:
            # name field is always sets for this invoices
            # common name structure is IT01234567890_01234.xml
            start = e_trasmission.name.find('_') + 1
            end = e_trasmission.name.rfind('.')
            e_trasmission.write({'communication_number': e_trasmission.name[start:end]})

    _log.info("Upgrade completed")
