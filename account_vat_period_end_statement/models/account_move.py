# -*- coding: utf-8 -*-

from openerp import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    vat_period_id = fields.Many2one(
        string=_('Vat Period'),
        comodel_name='account.period',
        states={'posted': [('readonly', True)]}
    )

    @api.model
    def create(self, vals):
        # By default, if vat_period_id is not specified,
        # it will be the same of period_id.
        # If period_id is empty too, we will compute the period from date.
        if not vals.get('vat_period_id', False):
            if vals.get('period_id', False):
                vals['vat_period_id'] = vals['period_id']
            elif vals.get('date', False):
                vals['vat_period_id'] = \
                    self.env['account.period'].find(vals['date']).id

        return super(AccountMove, self).create(vals)
