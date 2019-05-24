# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
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

from openerp import models, fields, api
from openerp.exceptions import ValidationError
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

try:
    import codicefiscale
except ImportError as err:
    _logger.debug(err)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def check_fiscalcode(self):
        for partner in self:
            if not partner.fiscalcode:
                return True
            elif len(partner.fiscalcode) != 16 and partner.individual:
                return False
            else:
                return True

    fiscalcode = fields.Char(
        'Fiscal Code', size=16, help="Italian Fiscal Code")
    individual = fields.Boolean(
        'Individual', default=False,
        help="If checked the C.F. is referred to a Individual Person")

    @api.one
    @api.constrains('fiscalcode', 'individual')
    def check_fiscalcode(self):
        if self.fiscalcode and len(self.fiscalcode) == 16:
            control_value = codicefiscale.control_code(self.fiscalcode[0:15])
            if self.fiscalcode[15:16] != control_value:
                value = self.fiscalcode[0:15] + control_value
                raise ValidationError(_(
                    'Invalid fiscalcode! \n Fiscal code could be %s' % value))

        elif self.individual:
            if len(self.fiscalcode) != 16:
                raise ValidationError(_(
                    'The fiscal code doesn\'t seem to be correct.'))

        elif self.fiscalcode:
            if self.country_id and self.country_id.code == self.fiscalcode[:2]:
                fiscalcode = self.fiscalcode[2:]
            else:
                fiscalcode = self.fiscalcode

            if len(fiscalcode) != 11:
                raise ValidationError(_(
                    'The fiscal code refers to a vat number '
                    'but doesn\'t seem to be correct.'))

            elif self.country_id and \
               not self.simple_vat_check(self.country_id.code, fiscalcode):
                raise ValidationError(_(
                    'The fiscal code is not a valid vat number!'))

    @api.multi
    def write(self, vals):
        if 'fiscalcode' in vals and isinstance(vals['fiscalcode'], basestring):
            # remove white space at the end of fiscalcode
            vals['fiscalcode'] = vals['fiscalcode'].rstrip()

        return super(ResPartner, self).write(vals)

