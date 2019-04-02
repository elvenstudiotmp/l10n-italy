# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openerp import models, _
from openerp.exceptions import ValidationError
from openerp.addons.l10n_it_fatturapa.bindings.fatturapa_v_1_2 import (
    DatiDDTType,
    DatiTrasportoType,
    DatiAnagraficiVettoreType,
    IdFiscaleType,
    AnagraficaType
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setDatiDDT(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiDDT(invoice, body)
        inv_lines_by_ddt = {}
        for line in invoice.invoice_line:
            for ddt in line.ddt_ids:
                key = (ddt.ddt_number, ddt.date[:10])
                if key not in inv_lines_by_ddt:
                    inv_lines_by_ddt[key] = []
                inv_lines_by_ddt[key].append(line.ftpa_line_number)

        # if at least one line has ddt info,
        # we must use DatiDDT section
        if inv_lines_by_ddt:
            for key in sorted(inv_lines_by_ddt.iterkeys()):
                DatiDDT = DatiDDTType(NumeroDDT=key[0], DataDDT=key[1])
                for line_number in inv_lines_by_ddt[key]:
                    DatiDDT.RiferimentoNumeroLinea.append(line_number)
                body.DatiGenerali.DatiDDT.append(DatiDDT)

        elif invoice.ddt_into_invoice:
            body.DatiGenerali.DatiTrasporto = DatiTrasportoType(
                MezzoTrasporto=invoice.transportation_method_id.name or None,
                CausaleTrasporto=invoice.transportation_reason_id.name or None,
                NumeroColli=invoice.parcels or None,
                Descrizione=invoice.goods_description_id.name or None,
                PesoLordo='%.2f' % invoice.gross_weight,
                PesoNetto='%.2f' % invoice.net_weight,
                TipoResa=None  # invoice.incoterms_id.code or None
            )
            if invoice.carrier_id:
                if not invoice.carrier_id.vat:
                    raise ValidationError(
                        _('TIN not set for %s.') % invoice.carrier_id.name)

                body.DatiGenerali.DatiTrasporto.DatiAnagraficiVettore = (
                    DatiAnagraficiVettoreType())
                if invoice.carrier_id.fiscalcode:
                    body.DatiGenerali.DatiTrasporto.DatiAnagraficiVettore.\
                        CodiceFiscale = invoice.carrier_id.fiscalcode
                body.DatiGenerali.DatiTrasporto.DatiAnagraficiVettore.\
                    IdFiscaleIVA = IdFiscaleType(
                        IdPaese=invoice.carrier_id.vat[0:2],
                        IdCodice=invoice.carrier_id.vat[2:]
                    )
                body.DatiGenerali.DatiTrasporto.DatiAnagraficiVettore.\
                    Anagrafica = AnagraficaType(
                        Denominazione=invoice.carrier_id.name)

        return res

