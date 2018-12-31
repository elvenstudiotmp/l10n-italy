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
from openerp.osv import fields, orm
from openerp.tools.translate import _


class RemovePeriod(orm.TransientModel):

    _name = 'remove.period.from.vat.commitment'

    def _get_period_ids(self, cr, uid, context=None):
        commitment_obj = self.pool['account.vat.communication']
        res = []
        if 'active_id' in context:
            commitment = commitment_obj.browse(
                cr, uid, context['active_id'], context)
            for period in commitment.period_ids:
                res.append((period.id, period.name))
        return res

    _columns = {
        'period_id': fields.selection(
            _get_period_ids, 'Period', required=True),
    }

    def remove_period(self, cr, uid, ids, context=None):
        if 'active_id' not in context:
            raise orm.except_orm(_('Error'), _('Current commitment not found'))
        self.pool['account.period'].write(
            cr, uid, [int(self.browse(cr, uid, ids, context)[0].period_id)],
            {'vat_commitment_id': False}, context=context
        )
        self.pool['account.vat.communication'].compute_amounts(
            cr, uid, [context['active_id']], context=context)
        return {
            'type': 'ir.actions.act_window_close',
        }
