# -*- coding: utf-8 -*-

import logging
# from openerp import api, SUPERUSER_ID

_log = logging.getLogger(__name__)


def migrate(cr, version):
    """Store vat period in invoices, account moves and account move lines"""
    if not version:
        return

    _log.info('Updating vat period in invoices...')
    cr.execute("""UPDATE account_invoice SET vat_period_id = period_id""")

    _log.info('Updating vat period in move entries...')
    cr.execute("""UPDATE account_move SET vat_period_id = period_id""")

    _log.info('Updating vat period in move lines...')
    cr.execute("""UPDATE account_move_line SET vat_period_id = period_id""")

    _log.info('Vat period update completed.')
