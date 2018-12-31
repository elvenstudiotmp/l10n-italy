# -*- coding: utf-8 -*-

from openerp import models, fields, _
from openerp.tools.sql import drop_view_if_exists


class ReportIntrastat(models.Model):
    _inherit = "report.intrastat"

    invoice_supplier_ref = fields.Char(
        readonly=True
    )

    invoice_type = fields.Selection(
        selection=[
            ('in_invoice', _('Purchase Invoice')),
            ('in_refund', _('Purchase Refund')),
            ('out_invoice', _('Sale Invoice')),
            ('out_refund', _('Sale Refund')),
        ],
        readonly=True
    )

    partner_id = fields.Many2one(
        string=_('Partner'),
        comodel_name='res.partner',
        readonly=True
    )

    partner_vat = fields.Char(
        string=_('VAT'),
        readonly=True
    )

    def init(self, cr):
        drop_view_if_exists(cr, 'report_intrastat')
        cr.execute("""
            create or replace view report_intrastat as (
                select
                    to_char(coalesce(inv.registration_date, inv.date_invoice, inv.create_date), 'YYYY') as name,
                    to_char(coalesce(inv.registration_date, inv.date_invoice, inv.create_date), 'MM') as month,
                    min(inv_line.id) as id,
                    intrastat.id as intrastat_id,
                    upper(inv_country.code) as code,
                    (
                      case when inv.type in ('in_refund', 'out_refund')
                          then -1
                          else 1
                      end
                    ) *
                    sum(
                      case when inv_line.price_unit is not null
                          then (inv_line.price_unit - (inv_line.price_unit * inv_line.discount / 100)) * inv_line.quantity
                          else 0
                        end
                    ) as value,
                    sum(
                        case when uom.category_id != puom.category_id 
                            then (pt.weight_net * inv_line.quantity)
                            else (pt.weight_net * inv_line.quantity * uom.factor) 
                        end
                    ) as weight,
                    sum(
                        case when uom.category_id != puom.category_id 
                            then inv_line.quantity
                            else (inv_line.quantity * uom.factor) 
                        end
                    ) as supply_units,
                    inv.supplier_invoice_number as invoice_supplier_ref,
                    inv.partner_id as partner_id,
                    inv_address.vat as partner_vat,
                    inv.currency_id as currency_id,
                    inv.number as ref,
                    case when inv.type in ('out_invoice','out_refund')
                        then 'export'
                        else 'import'
                    end as type,
                    inv.type as invoice_type
                from
                    account_invoice inv
                    left join account_invoice_line inv_line on inv_line.invoice_id=inv.id
                    left join (product_template pt
                        left join product_product pp on (pp.product_tmpl_id = pt.id))
                    on (inv_line.product_id = pp.id)
                    left join product_uom uom on uom.id=inv_line.uos_id
                    left join product_uom puom on puom.id = pt.uom_id
                    left join report_intrastat_code intrastat on pt.intrastat_id = intrastat.id
                    left join (res_partner inv_address
                        left join res_country inv_country on (inv_country.id = inv_address.country_id))
                    on (inv_address.id = inv.partner_id)
                where
                    inv.state in ('open','paid')
                    and inv_line.product_id is not null
                    and inv_country.intrastat=true
                group by 
                  to_char(coalesce(inv.registration_date, inv.date_invoice, inv.create_date), 'YYYY'), 
                  to_char(coalesce(inv.registration_date, inv.date_invoice, inv.create_date), 'MM'), 
                  intrastat.id,
                  inv.type,
                  pt.intrastat_id, 
                  inv_country.code,
                  inv.partner_id,
                  inv_address.vat,
                  inv.number,
                  inv.supplier_invoice_number,
                  inv.currency_id
            )""")

