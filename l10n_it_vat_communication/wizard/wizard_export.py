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
# from openerp import release
import logging
# import pdb
_logger = logging.getLogger(__name__)
try:
    from unidecode import unidecode
    from openerp.addons.l10n_it_ade.bindings.dati_fattura_v_2_0 import (
        DatiFattura,
        VersioneType,
        DatiFatturaHeaderType,
        DichiaranteType,
        CodiceFiscaleType,
        DTEType,
        CedentePrestatoreDTEType,
        IdentificativiFiscaliType,
        IdentificativiFiscaliITType,
        IdFiscaleITType,
        IdFiscaleType,
        CessionarioCommittenteDTEType,
        AltriDatiIdentificativiNoSedeType,
        AltriDatiIdentificativiNoCAPType,
        IdentificativiFiscaliNoIVAType,
        IndirizzoType,
        IndirizzoNoCAPType,
        # RettificaType,
        DatiFatturaBodyDTEType,
        DatiGeneraliType,
        DatiRiepilogoType,
        DatiIVAType,
        DTRType,
        ANNType,
        CessionarioCommittenteDTRType,
        CedentePrestatoreDTRType,
        DatiFatturaBodyDTRType,
        DatiGeneraliDTRType,
    )
except ImportError as err:
    _logger.debug(err)

_logger.setLevel(logging.DEBUG)

VERSIONE = 'DAT20'


class WizardVatCommunication(orm.TransientModel):
    _name = "wizard.vat.communication"

    _columns = {
        'data': fields.binary("File", readonly=True),
        'name': fields.char('Filename', 32, readonly=True),

        'id_file': fields.char(_("ID File")),
        'position': fields.integer(_('Position')),  # todo help

        'state': fields.selection((
            ('create', _('Create File')),  # choose
            ('get', _('Download')),  # get the file
        )),
        'target': fields.char('Customers/Suppliers', 4, readonly=True),
    }

    _defaults = {
        'state': lambda *a: 'create',
        'position': 0,
    }

    def str60Latin(self, s):
        # t = s.encode('latin-1', 'ignore')
        return unidecode(s)[:60]

    def str80Latin(self, s):
        return unidecode(s)[:80]

    def get_dati_fattura_header(self, cr, uid,
                                commitment_model, commitment, context=None):
        context = context or {}
        fields = commitment_model.get_xml_fattura_header(
            cr, uid, commitment, context)
        header = (DatiFatturaHeaderType())
        if 'xml_CodiceFiscale' in fields:
            header.Dichiarante = (DichiaranteType())
            header.Dichiarante.Carica = fields['xml_Carica']
            header.Dichiarante.CodiceFiscale = CodiceFiscaleType(
                fields['xml_CodiceFiscale'])
        return header

    def get_sede(self, cr, uid, fields, dte_dtr_id, selector, context=None):
        if dte_dtr_id == 'DTE':
            if selector == 'company':
                sede = (IndirizzoType())
            elif selector == 'customer':
                sede = (IndirizzoNoCAPType())
            elif selector == 'supplier':
                sede = (IndirizzoType())
            else:
                raise orm.except_orm(
                    _('Error!'),
                    _('Internal error: invalid partner selector'))
        else:
            if selector == 'company':
                sede = (IndirizzoType())
            elif selector == 'customer':
                sede = (IndirizzoNoCAPType())
            elif selector == 'supplier':
                sede = (IndirizzoNoCAPType())
            else:
                raise orm.except_orm(
                    _('Error!'),
                    _('Internal error: invalid partner selector'))

        if fields.get('xml_Indirizzo'):
            sede.Indirizzo = self.str60Latin(fields['xml_Indirizzo'])
        else:
            raise orm.except_orm(
                _('Error!'),
                _('Missed address %s %s %S' %
                  (fields.get('xml_Denominazione'),
                   fields.get('xml_Nome'),
                   fields.get('xml_Cognome'))))
        if fields.get('xml_Comune'):
            sede.Comune = self.str60Latin(fields['xml_Comune'])
        else:
            raise orm.except_orm(
                _('Error!'),
                _('Missed city %s %s %S' %
                  (fields.get('xml_Denominazione'),
                   fields.get('xml_Nome'),
                   fields.get('xml_Cognome'))))
        if fields.get('xml_CAP') and fields['xml_Nazione'] == 'IT':
            sede.CAP = fields['xml_CAP']
        elif selector == 'company':
            raise orm.except_orm(
                _('Error!'),
                _('Missed company zip code'))
        if fields.get('xml_Provincia') and fields['xml_Nazione'] == 'IT':
            sede.Provincia = fields['xml_Provincia']

        sede.Nazione = fields['xml_Nazione']
        return sede

    def get_name(self, cr, uid, fields, dte_dtr_id, selector, context=None):
        if dte_dtr_id == 'DTE':
            if selector == 'company':
                AltriDatiIdentificativi = (AltriDatiIdentificativiNoSedeType())
            elif selector == 'customer' or selector == 'supplier':
                AltriDatiIdentificativi = (AltriDatiIdentificativiNoCAPType())
            else:
                raise orm.except_orm(
                    _('Error!'),
                    _('Internal error: invalid partner selector'))
        else:
            if selector == 'company':
                AltriDatiIdentificativi = (AltriDatiIdentificativiNoSedeType())
            elif selector == 'customer' or selector == 'supplier':
                AltriDatiIdentificativi = (AltriDatiIdentificativiNoCAPType())
            else:
                raise orm.except_orm(
                    _('Error!'),
                    _('Internal error: invalid partner selector'))

        if 'xml_Denominazione' in fields:
            AltriDatiIdentificativi.Denominazione = self.str80Latin(
                fields['xml_Denominazione'])
        else:
            AltriDatiIdentificativi.Nome = self.str60Latin(
                fields['xml_Nome'])
            AltriDatiIdentificativi.Cognome = self.str60Latin(
                fields['xml_Cognome'])
        AltriDatiIdentificativi.Sede = self.get_sede(
            cr, uid, fields, dte_dtr_id, selector, context=context)
        return AltriDatiIdentificativi

    def get_cedente_prestatore(self, cr, uid,
                               fields, dte_dtr_id,
                               context=None):

        if dte_dtr_id == 'DTE':
            CedentePrestatore = (CedentePrestatoreDTEType())
            CedentePrestatore.IdentificativiFiscali = (
                IdentificativiFiscaliITType())
            # Company VAT number must be present
            CedentePrestatore.IdentificativiFiscali.IdFiscaleIVA = (
                IdFiscaleITType())
            partner_type = 'company'
        elif dte_dtr_id == 'DTR':
            CedentePrestatore = (CedentePrestatoreDTRType())
            CedentePrestatore.IdentificativiFiscali = (
                IdentificativiFiscaliType())
            # Company VAT number must be present
            CedentePrestatore.IdentificativiFiscali.IdFiscaleIVA = (
                IdFiscaleType())
            partner_type = 'supplier'
        else:
            raise orm.except_orm(
                _('Error!'),
                _('Internal error: invalid partner selector'))

        if fields.get('xml_IdPaese') and fields.get('xml_IdCodice'):
            CedentePrestatore.IdentificativiFiscali.IdFiscaleIVA.\
                IdPaese = fields['xml_IdPaese']
            CedentePrestatore.IdentificativiFiscali.IdFiscaleIVA.\
                IdCodice = fields['xml_IdCodice']
        if fields.get('xml_CodiceFiscale'):
            CedentePrestatore.IdentificativiFiscali.CodiceFiscale = \
                CodiceFiscaleType(fields['xml_CodiceFiscale'])
        CedentePrestatore.AltriDatiIdentificativi = \
            self.get_name(cr, uid, fields, dte_dtr_id, partner_type, context)
        return CedentePrestatore

    def get_cessionario_committente(self, cr, uid,
                                    fields, dte_dtr_id,
                                    context=None):

        if dte_dtr_id == 'DTE':
            partner = (CessionarioCommittenteDTEType())
            partner_type = 'customer'
            partner.IdentificativiFiscali = (IdentificativiFiscaliNoIVAType())
        else:
            # DTR
            partner = (CessionarioCommittenteDTRType())
            partner_type = 'company'
            partner.IdentificativiFiscali = (IdentificativiFiscaliITType())

        if fields.get('xml_IdPaese') and fields.get('xml_IdCodice'):
            if dte_dtr_id == 'DTE':
                partner.IdentificativiFiscali.IdFiscaleIVA = (IdFiscaleType())
            else:
                partner.IdentificativiFiscali.IdFiscaleIVA = (
                    IdFiscaleITType())

            partner.IdentificativiFiscali.IdFiscaleIVA.\
                IdPaese = fields['xml_IdPaese']
            partner.IdentificativiFiscali.IdFiscaleIVA.\
                IdCodice = fields['xml_IdCodice']

            if fields.get('xml_IdPaese') == 'IT' and fields.get(
                    'xml_CodiceFiscale'):
                partner.IdentificativiFiscali.\
                    CodiceFiscale = CodiceFiscaleType(
                        fields['xml_CodiceFiscale'])
        else:
            partner.IdentificativiFiscali.CodiceFiscale = CodiceFiscaleType(
                fields['xml_CodiceFiscale'])
        # row 44: 2.2.2   <AltriDatiIdentificativi>
        partner.AltriDatiIdentificativi = \
            self.get_name(cr, uid, fields, dte_dtr_id, partner_type, context)
        return partner

    def get_ann(self, cr, uid, commitment_model, commitment, id_file, position=None, context=None):
        context = context or {}
        ann = (ANNType())
        ann.IdFile = id_file

        if position:
            ann.Posizione = position

        return ann

    def get_dte_dtr(self, cr, uid, commitment_model, commitment, dte_dtr_id, context=None):
        context = context or {}
        res_partner_model = self.pool['res.partner']

        partners = []
        partner_ids = commitment_model.get_partner_list(
            cr, uid, commitment, dte_dtr_id, context)
        for partner_id in partner_ids:
            fields = commitment_model.get_xml_cessionario_cedente(
                cr, uid, commitment, partner_id, dte_dtr_id, context)

            # Missed mandatory data: skip record
            # if not fields.get('xml_IdPaese') and \
            #         not fields.get('xml_IdCodice') and \
            #         not fields.get('xml_CodiceFiscale', False):
            #     # Corrispettivi
            #     continue
            # TODO: StabileOrganizzazione
            # TODO: RappresentanteFiscale

            if not 'xml_Denominazione' in fields:
                if not 'xml_Nome' in fields or not 'xml_Cognome' in fields or not fields['xml_Nome'] or not fields['xml_Cognome']:

                    partner = res_partner_model.browse(cr, uid, partner_id)
                    raise orm.except_orm(
                        _('Error!'),
                        _('Partner %s doe not have a valid name or surname!') % (partner.name)
                    )

            if dte_dtr_id == 'DTE':
                partner = self.get_cessionario_committente(
                    cr, uid, fields, dte_dtr_id, context)
            else:
                partner = self.get_cedente_prestatore(
                    cr, uid, fields, dte_dtr_id, context
                )

            invoices = []
            # Iterate over invoices of current partner
            invoice_ids = commitment_model.get_invoice_list(
                cr, uid, commitment, partner_id, dte_dtr_id, context)

            if not invoice_ids:
                # skip this partner because no invoices are related to it
                continue

            for invoice_id in invoice_ids:
                fields = commitment_model.get_xml_invoice(
                    cr, uid, commitment, invoice_id, dte_dtr_id, context)
                if dte_dtr_id == 'DTE':
                    invoice = (DatiFatturaBodyDTEType())
                    invoice.DatiGenerali = (DatiGeneraliType())
                else:
                    invoice = (DatiFatturaBodyDTRType())
                    invoice.DatiGenerali = (DatiGeneraliDTRType())

                invoice.DatiGenerali.TipoDocumento = fields[
                    'xml_TipoDocumento']
                invoice.DatiGenerali.Data = fields['xml_Data']
                invoice.DatiGenerali.Numero = fields['xml_Numero']
                if dte_dtr_id == 'DTR':
                    invoice.DatiGenerali.DataRegistrazione = fields[
                        'xml_DataRegistrazione']

                dati_riepilogo = []
                line_ids = commitment_model.get_riepilogo_list(
                    cr, uid, commitment, invoice_id, dte_dtr_id, context)
                for line_id in line_ids:
                    fields = commitment_model.get_xml_riepilogo(
                        cr, uid, commitment, line_id, dte_dtr_id, context)
                    riepilogo = (DatiRiepilogoType())
                    riepilogo.ImponibileImporto = '{:.2f}'.format(
                        fields['xml_ImponibileImporto'])
                    riepilogo.DatiIVA = (DatiIVAType())
                    riepilogo.DatiIVA.Imposta = '{:.2f}'.format(
                        fields['xml_Imposta'])
                    riepilogo.DatiIVA.Aliquota = '{:.2f}'.format(
                        fields['xml_Aliquota'])
                    if 'xml_Detraibile' in fields:
                        riepilogo.Detraibile = '{:.2f}'.format(
                            fields['xml_Detraibile'])
                    if 'xml_Deducibile' in fields:
                        riepilogo.Deducibile = fields['xml_Deducibile']
                    if 'xml_Natura' in fields:
                        riepilogo.Natura = fields['xml_Natura']
                    riepilogo.EsigibilitaIVA = fields['xml_EsigibilitaIVA']
                    dati_riepilogo.append(riepilogo)
                invoice.DatiRiepilogo = dati_riepilogo
                invoices.append(invoice)

            if dte_dtr_id == 'DTE':
                partner.DatiFatturaBodyDTE = invoices
            else:
                partner.DatiFatturaBodyDTR = invoices
            partners.append(partner)

        fields = commitment_model.get_xml_company(
            cr, uid, commitment, dte_dtr_id, context)
        if dte_dtr_id == 'DTE':
            dte = (DTEType())

            dte.CedentePrestatoreDTE = self.get_cedente_prestatore(
                cr, uid, fields, dte_dtr_id, context)
            dte.CessionarioCommittenteDTE = partners

            # dte.Rettifica = (RettificaType())

            return dte
        else:
            dtr = (DTRType())

            dtr.CessionarioCommittenteDTR = self.get_cessionario_committente(
                cr, uid, fields, dte_dtr_id, context
            )

            dtr.CedentePrestatoreDTR = partners

            # dtr.Rettifica = (RettificaType())

            return dtr

    def export_vat_communication_DTE(self, cr, uid, ids, context=None):
        context = context or {}
        context['dte_dtr_id'] = 'DTE'
        return self.export_vat_communication(cr, uid, ids, context)

    def export_vat_communication_DTR(self, cr, uid, ids, context=None):
        context = context or {}
        context['dte_dtr_id'] = 'DTR'
        return self.export_vat_communication(cr, uid, ids, context)

    def export_vat_communication_ANN(self, cr, uid, ids, context=None):
        context = context or {}
        context['dte_dtr_id'] = 'ANN'
        return self.export_vat_communication(cr, uid, ids, context)

    def export_vat_communication(self, cr, uid, ids, context=None):
        context = context or {}
        dte_dtr_id = context.get('dte_dtr_id', 'DTE')
        commitment_model = self.pool['account.vat.communication']
        commitment_ids = context.get('active_ids', False)
        if commitment_ids:
            for commitment in commitment_model.browse(
                    cr, uid, commitment_ids, context=context):

                communication = DatiFattura()
                communication.versione = VersioneType(VERSIONE)
                communication.DatiFatturaHeader = self.get_dati_fattura_header(cr, uid, commitment_model, commitment)

                if dte_dtr_id == 'DTE':
                    communication.DTE = self.get_dte_dtr(cr, uid, commitment_model, commitment, dte_dtr_id, context=context)

                elif dte_dtr_id == 'DTR':
                    communication.DTR = self.get_dte_dtr(cr, uid, commitment_model, commitment, dte_dtr_id, context=context)

                elif dte_dtr_id == 'ANN':
                    wizard = self.browse(cr, uid, ids, context=context)
                    communication.ANN = self.get_ann(cr, uid, commitment_model, commitment, wizard.id_file, wizard.position, context=context)

                else:
                    raise orm.except_orm(
                        _('Error!'),
                        _('Internal error: invalid partner selector (%s)' % dte_dtr_id)
                    )

                # file_name = 'Comunicazine_IVA-{}.xml'.format(
                #     commitment.progressivo_telematico)
                progr_invio = commitment_model.set_progressivo_telematico(
                    cr, uid, commitment, context)
                file_name = 'IT%s_DF_%s.xml' % (
                    commitment.soggetto_codice_fiscale, progr_invio)
                vat_communication_xml = communication.toDOM().toprettyxml(
                    encoding="latin1")

                out = vat_communication_xml.encode("base64")

                attach_vals = {
                    'name': file_name,
                    'datas_fname': file_name,
                    'datas': out,
                    'res_model': 'account.vat.communication',
                    'res_id': commitment.id,
                    'type': 'binary',
                }

                self.pool['ir.attachment'].create(cr, uid, attach_vals)

                return self.write(
                    cr, uid, ids, {
                        'state': 'get',
                        'data': out,
                        'name': file_name,
                        'target': dte_dtr_id,
                    }, context=context
                )
