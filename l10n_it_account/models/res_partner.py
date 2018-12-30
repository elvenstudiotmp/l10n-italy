# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2018 Elven Studio (<http://www.elvenstudio.it>).
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
#

from openerp import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        if 'vat' in vals and isinstance(vals['vat'], basestring):
            # remove white space at the end of vat
            vals['vat'] = vals['vat'].rstrip()

        return super(ResPartner, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'vat' in vals and isinstance(vals['vat'], basestring):
            # remove white space at the end of vat
            vals['vat'] = vals['vat'].rstrip()

        return super(ResPartner, self).write(vals)
