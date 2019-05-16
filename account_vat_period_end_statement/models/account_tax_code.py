# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class AccountTaxCode(osv.osv):
    _inherit = 'account.tax.code'

    def _sum_vat_period(self, cr, uid, ids, name, args, context):
        # Perform the same computation of sum_period field.
        # but instead of filter by period_id, we will use vat_period_id

        if context is None:
            context = {}
        move_state = ('posted', )
        if context.get('state', False) == 'all':
            move_state = ('draft', 'posted', )
        if context.get('period_id', False):
            period_id = context['period_id']
        else:
            period_id = self.pool.get('account.period').find(cr, uid, context=context)
            if not period_id:
                return dict.fromkeys(ids, 0.0)
            period_id = period_id[0]
        return self._sum(
            cr, uid, ids, name, args, context,
            where=' AND line.vat_period_id=%s AND move.state IN %s',
            where_params=(period_id, move_state))

    _columns = {
        'sum_vat_period': fields.function(_sum_vat_period, string="Vat Period Sum")
    }
