# -*- coding: utf-8 -*-

from openerp import models, fields, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_bill_of_entry_tax = fields.Boolean(
        help=_(
            'Set if this product is a custom tax '
            'or a bill of entry shipping tax'
        )
    )
