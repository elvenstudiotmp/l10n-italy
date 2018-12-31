# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017    SHS-AV s.r.l. <https://www.zeroincombenze.it>
#    Copyright (C) 2012-15 Agile Business Group sagl <http://www.agilebg.com>
#    Copyright (C) 2013-15 LinkIt Spa <http://http://www.linkgroup.it>
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


class AddPeriod(orm.TransientModel):

    _name = 'add.period.to.vat.commitment'

    _columns = {
        'period_id': fields.many2one(
            'account.period', 'Period', required=True),
    }

    def add_period(self, cr, uid, ids, context=None):
        if 'active_id' not in context:
            raise orm.except_orm(_('Error'), _('Current commitment not found'))

        wizard = self.browse(cr, uid, ids, context)[0]
        if wizard.period_id.vat_commitment_id:
            raise orm.except_orm(
                _('Error'),
                _('Period %s is already associated to commitment') %
                (wizard.period_id.name),
            )

        commitment_cls = self.pool['account.vat.communication']
        commitment = commitment_cls.browse(
            cr, uid, context['active_id'], context=context)

        wizard.period_id.write({'vat_commitment_id': context['active_id']})
        self.pool['account.vat.communication'].compute_amounts(
            cr, uid, [context['active_id']], context=context)

        # can compute partner list only after adding commitment to period
        if len(commitment_cls.get_partner_list(cr, uid, commitment, 'DTE', context=context)) > 1000 or \
           len(commitment_cls.get_partner_list(cr, uid, commitment, 'DTR', context=context)) > 1000:
            raise orm.except_orm(
                _('Error'),
                _('Maximum partners number reached!')
            )

        return {
            'type': 'ir.actions.act_window_close',
        }
