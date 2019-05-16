# -*- coding: utf-8 -*-

from openerp import models, fields, api, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    vat_period_id = fields.Many2one(
        string=_('Vat Period'),
        comodel_name='account.period',
        readonly=True
    )

    @api.model
    def create(self, vals):
        # By default, if vat_period_id is not specified,
        # it will be the same of vat_period_id of the linked move_id.
        if not vals.get('vat_period_id', False):
            if vals.get('move_id', False):
                move = self.env['account.move'].browse(vals['move_id'])
                if move.vat_period_id:
                    vals['vat_period_id'] = move.vat_period_id.id

            # If vat_period_id is empty in move_id,
            # we will use period_id from the move_id or
            # the period computed from date.
            if not vals.get('vat_period_id', False):
                if vals.get('period_id', False):
                    vals['vat_period_id'] = vals['period_id']
                elif vals.get('date', False):
                    vals['vat_period_id'] = \
                        self.env['account.period'].find(vals['date']).id

        return super(AccountMoveLine, self).create(vals)
