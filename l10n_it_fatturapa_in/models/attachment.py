# -*- coding: utf-8 -*-

import base64
from openerp import fields, models, api, _
from openerp.exceptions import ValidationError


class FatturaPAAttachmentIn(models.Model):
    _name = "fatturapa.attachment.in"
    _description = "FatturaPA import File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']
    _order = 'id desc'

    ir_attachment_id = fields.Many2one(
        'ir.attachment', 'Attachment', required=True, ondelete="cascade")
    in_invoice_ids = fields.One2many(
        'account.invoice', 'fatturapa_attachment_in_id',
        string="In Invoices", readonly=True)
    xml_supplier_id = fields.Many2one(
        "res.partner", string="Supplier", compute="_compute_xml_data",
        store=True)
    invoices_number = fields.Integer(
        "Invoices number", compute="_compute_xml_data", store=True)
    invoices_total = fields.Float(
        "Invoices total", compute="_compute_xml_data", store=True,
        help="Se indicato dal fornitore, Importo totale del documento al "
             "netto dell'eventuale sconto e comprensivo di imposta a debito "
             "del cessionario / committente"
    )
    registered = fields.Boolean(
        "Registered", compute="_compute_registered", store=True)

    @api.onchange('datas_fname')
    def onchagne_datas_fname(self):
        self.name = self.datas_fname

    def get_xml_string(self):
        return self.ir_attachment_id.get_xml_string()

    @api.multi
    @api.depends('ir_attachment_id.datas')
    def _compute_xml_data(self):
        for att in self:
            fatt = self.env['wizard.import.fatturapa'].get_invoice_obj(att)
            cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore
            partner_id = self.env['wizard.import.fatturapa'].getCedPrest(
                cedentePrestatore)
            att.xml_supplier_id = partner_id
            att.invoices_number = len(fatt.FatturaElettronicaBody)
            att.invoices_total = 0
            for invoice_body in fatt.FatturaElettronicaBody:
                att.invoices_total += float(
                    invoice_body.DatiGenerali.DatiGeneraliDocumento.
                    ImportoTotaleDocumento or 0
                )

    @api.multi
    @api.depends('in_invoice_ids', 'invoices_number')
    def _compute_registered(self):
        for att in self:
            if (
                att.in_invoice_ids and
                len(att.in_invoice_ids) == att.invoices_number
            ):
                att.registered = True
            else:
                att.registered = False

    def extract_attachments(self, AttachmentsData, invoice_id):
        AttachModel = self.env['fatturapa.attachments']
        for attach in AttachmentsData:
            if not attach.NomeAttachment:
                name = _("Attachment without name")
            else:
                name = attach.NomeAttachment
            content = attach.Attachment
            _attach_dict = {
                'name': name,
                'datas': base64.b64encode(str(content)),
                'datas_fname': name,
                'description': attach.DescrizioneAttachment or '',
                'compression': attach.AlgoritmoCompressione or '',
                'format': attach.FormatoAttachment or '',
                'invoice_id': invoice_id,
            }
            AttachModel.create(_attach_dict)

    @api.multi
    def action_show_preview(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.ftpa_preview_link,
            'target': 'new',
        }

    @api.multi
    def action_show_invoices(self):
        self.ensure_one()
        if not self.in_invoice_ids:
            raise ValidationError(_('No invoices to show!'))

        action = self.env['ir.model.data']\
            .get_object_reference('account', 'action_invoice_tree2')
        action_id = action and action[1] or False
        result = self.env['ir.actions.act_window'].browse(action_id).read()[0]
        result['domain'] = "[('id','in'," + str(self.in_invoice_ids.ids) + ")]"
        return result

    @api.multi
    def action_recompute_fatturapa_data(self):
        self.ensure_one()
        self._compute_xml_data()
        return True
