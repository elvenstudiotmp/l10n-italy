# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2012 Domsense s.r.l. (<http://www.domsense.com>).
#    Copyright (C) 2012-15 Agile Business Group sagl (<http://www.agilebg.com>)
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
#

import math

from openerp.osv import orm, fields
from openerp.tools.translate import _
from openerp.addons.decimal_precision import decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

try:
    import codicefiscale
except ImportError as err:
    _logger.debug(err)


class AccountVatPeriodEndStatement(orm.Model):

    def _compute_authority_vat_amount(
        self, cr, uid, ids, field_name, arg, context
    ):
        res = {}
        for i in ids:
            statement = self.browse(cr, uid, i)
            debit_vat_amount = 0.0
            credit_vat_amount = 0.0
            generic_vat_amount = 0.0
            for debit_line in statement.debit_vat_account_line_ids:
                debit_vat_amount += debit_line.amount
            for credit_line in statement.credit_vat_account_line_ids:
                credit_vat_amount += credit_line.amount
            for generic_line in statement.generic_vat_account_line_ids:
                generic_vat_amount += generic_line.amount
            authority_amount = (
                debit_vat_amount - credit_vat_amount - generic_vat_amount -
                statement.previous_credit_vat_amount +
                statement.previous_debit_vat_amount)
            res[i] = authority_amount
        return res

    def _compute_payable_vat_amount(
        self, cr, uid, ids, field_name, arg, context
    ):
        res = {}
        for i in ids:
            statement = self.browse(cr, uid, i)
            debit_vat_amount = 0.0
            for debit_line in statement.debit_vat_account_line_ids:
                debit_vat_amount += debit_line.amount
            res[i] = debit_vat_amount
        return res

    def _compute_deductible_vat_amount(
        self, cr, uid, ids, field_name, arg, context
    ):
        res = {}
        for i in ids:
            statement = self.browse(cr, uid, i)
            credit_vat_amount = 0.0
            for credit_line in statement.credit_vat_account_line_ids:
                credit_vat_amount += credit_line.amount
            res[i] = credit_vat_amount
        return res

    # Workflow stuff
    #

    def _reconciled(self, cr, uid, ids, name, args, context=None):
        res = {}
        for rec_id in ids:
            res[rec_id] = self.test_paid(cr, uid, [rec_id])
        return res

    def _is_summary_statement(self, cr, uid, ids, name, args, context=None):
        res = {}

        statements = self.browse(cr, uid, ids, context=context)
        for statement in statements:

            is_summary = False
            if statement.period_ids and len(statement.period_ids) == 1 and statement.period_ids.special:
                is_summary = True

            res[statement.id] = is_summary

        return res

    def move_line_id_payment_gets(self, cr, uid, ids, *args):
        res = {}
        if not ids:
            return res
        cr.execute('SELECT statement.id, l.id '
                   'FROM account_move_line l '
                   'LEFT JOIN account_vat_period_end_statement statement ON '
                   '(statement.move_id=l.move_id) '
                   'WHERE statement.id IN %s '
                   'AND l.account_id=statement.authority_vat_account_id',
                   (tuple(ids),))
        for r in cr.fetchall():
            res.setdefault(r[0], [])
            res[r[0]].append(r[1])
        return res

    # return the ids of the move lines which has the same account than the
    # statement
    # whose id is in ids
    def move_line_id_payment_get(self, cr, uid, ids, *args):
        if not ids:
            return []
        result = self.move_line_id_payment_gets(cr, uid, ids, *args)
        return result.get(ids[0], [])

    def test_paid(self, cr, uid, ids, *args):
        res = self.move_line_id_payment_get(cr, uid, ids)
        if not res:
            return False
        ok = True
        for rec_id in res:
            cr.execute(
                'select reconcile_id from account_move_line where id=%s',
                (rec_id,))
            ok = ok and bool(cr.fetchone()[0])
        return ok

    def _get_statement_from_line(self, cr, uid, ids, context=None):
        move = {}
        for line in self.pool.get('account.move.line').browse(
            cr, uid, ids, context=context
        ):
            if line.reconcile_partial_id:
                for line2 in line.reconcile_partial_id.line_partial_ids:
                    move[line2.move_id.id] = True
            if line.reconcile_id:
                for line2 in line.reconcile_id.line_id:
                    move[line2.move_id.id] = True
        statement_ids = []
        if move:
            statement_ids = self.pool.get(
                'account.vat.period.end.statement').search(
                cr, uid, [('move_id', 'in', move.keys())], context=context)
        return statement_ids

    def _get_statement_from_move(self, cr, uid, ids, context=None):
        move = {}
        statement_ids = []
        for move in self.pool.get('account.move').browse(
            cr, uid, ids, context=context
        ):
            found_ids = self.pool.get(
                'account.vat.period.end.statement').search(
                cr, uid, [('move_id', '=', move.id)], context=context)
            for found_id in found_ids:
                if found_id not in statement_ids:
                    statement_ids.append(found_id)
        return statement_ids

    def _get_statement_from_reconcile(self, cr, uid, ids, context=None):
        move = {}
        for r in self.pool.get('account.move.reconcile').browse(
            cr, uid, ids, context=context
        ):
            for line in r.line_partial_ids:
                move[line.move_id.id] = True
            for line in r.line_id:
                move[line.move_id.id] = True

        statement_ids = []
        if move:
            statement_ids = self.pool.get(
                'account.vat.period.end.statement').search(
                cr, uid, [('move_id', 'in', move.keys())], context=context)
        return statement_ids

    def _get_credit_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('statement.credit.account.line').browse(
            cr, uid, ids, context=context
        ):
            result[line.statement_id.id] = True
        return result.keys()

    def _get_debit_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('statement.debit.account.line').browse(
            cr, uid, ids, context=context
        ):
            result[line.statement_id.id] = True
        return result.keys()

    def _get_generic_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('statement.generic.account.line').browse(
            cr, uid, ids, context=context
        ):
            result[line.statement_id.id] = True
        return result.keys()

    def _amount_residual(self, cr, uid, ids, name, args, context=None):
        result = {}
        for statement in self.browse(cr, uid, ids, context=context):
            result[statement.id] = 0.0
            if statement.move_id:
                for m in statement.move_id.line_id:
                    if m.account_id.type in ('receivable', 'payable'):
                        result[statement.id] += m.amount_residual_currency
        return result

    def _compute_name(self, cr, uid, ids, name, args, context=None):
        result = {}
        for statement in self.browse(cr, uid, ids, context=context):
            # todo format date
            result[statement.id] = _('Vat Statement of %s') % (statement.date if statement.date else '')
        return result

    def _compute_lines(self, cr, uid, ids, name, args, context=None):
        result = {}
        for statement in self.browse(cr, uid, ids, context=context):
            src = []
            lines = []
            if statement.move_id:
                for m in statement.move_id.line_id:
                    temp_lines = []
                    if m.reconcile_id:
                        temp_lines = map(
                            lambda x: x.id, m.reconcile_id.line_id)
                    elif m.reconcile_partial_id:
                        temp_lines = map(
                            lambda x: x.id,
                            m.reconcile_partial_id.line_partial_ids)
                    lines += [x for x in temp_lines if x not in lines]
                    src.append(m.id)

            lines = filter(lambda x: x not in src, lines)
            result[statement.id] = lines
        return result

    def _get_default_interest(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        company = user.company_id
        return company.of_account_end_vat_statement_interest

    def _get_default_interest_percent(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        company = user.company_id
        if not company.of_account_end_vat_statement_interest:
            return 0
        return company.of_account_end_vat_statement_interest_percent

    def _get_default_tax_authority(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        return user.company_id.of_account_end_vat_statement_tax_authority.id

    def _get_default_journal_id(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        return user.company_id.of_account_end_vat_statement_journal_id.id

    _name = "account.vat.period.end.statement"
    _rec_name = 'name'
    _order = 'date desc'
    _columns = {
        'name': fields.function(_compute_name, type='char', method=True, string='Name'),

        'debit_vat_account_line_ids': fields.one2many(
            'statement.debit.account.line', 'statement_id', 'Debit VAT',
            help='The accounts containing the debit VAT amount to write-off',
            states={
                'confirmed': [('readonly', True)],
                'paid': [('readonly', True)],
                'draft': [('readonly', False)]
            }),

        'credit_vat_account_line_ids': fields.one2many(
            'statement.credit.account.line', 'statement_id', 'Credit VAT',
            help='The accounts containing the credit VAT amount to write-off',
            states={
                'confirmed': [('readonly', True)],
                'paid': [('readonly', True)],
                'draft': [('readonly', False)]
            }),

        'previous_credit_vat_account_id': fields.many2one(
            'account.account', 'Previous Credits VAT',
            help='Credit VAT from previous periods',
            states={
                'confirmed': [('readonly', True)],
                'paid': [('readonly', True)],
                'draft': [('readonly', False)]
            }),
        'previous_credit_vat_amount': fields.float(
            'Previous Credits VAT Amount',
            states={
                'confirmed': [('readonly', True)],
                'paid': [('readonly', True)],
                'draft': [('readonly', False)]
            },
            digits_compute=dp.get_precision('Account')),

        'previous_debit_vat_account_id': fields.many2one(
            'account.account', 'Previous Debits VAT',
            help='Debit VAT from previous periods',
            states={
                'confirmed': [('readonly', True)],
                'paid': [('readonly', True)],
                'draft': [('readonly', False)]
            }),
        'previous_debit_vat_amount': fields.float(
            'Previous Debits VAT Amount',
            states={
                'confirmed': [('readonly', True)],
                'paid': [('readonly', True)],
                'draft': [('readonly', False)]
            },
            digits_compute=dp.get_precision('Account')),

        'generic_vat_account_line_ids': fields.one2many(
            'statement.generic.account.line', 'statement_id',
            'Other VAT Credits / Debits or Tax Compensations',
            states={
                'confirmed': [('readonly', True)],
                'paid': [('readonly', True)],
                'draft': [('readonly', False)]}),

        'authority_partner_id': fields.many2one(
            'res.partner', 'Tax Authority Partner',
            states={
                'confirmed': [('readonly', True)],
                'paid': [('readonly', True)],
                'draft': [('readonly', False)]}),
        'authority_vat_account_id': fields.many2one(
            'account.account', 'Tax Authority VAT Account', required=True,
            states={
                'confirmed': [('readonly', True)],
                'paid': [('readonly', True)],
                'draft': [('readonly', False)]}),
        'authority_vat_amount': fields.function(
            _compute_authority_vat_amount, method=True,
            string='Authority VAT Amount'),
        'payable_vat_amount': fields.function(
            _compute_payable_vat_amount, method=True,
            string='Payable VAT Amount'),
        'deductible_vat_amount': fields.function(
            _compute_deductible_vat_amount, method=True,
            string='Deductible VAT Amount'),

        'journal_id': fields.many2one(
            'account.journal', 'Journal', required=True,
            states={
                'confirmed': [('readonly', True)],
                'paid': [('readonly', True)],
                'draft': [('readonly', False)]}),
        'date': fields.date(
            'Date', required=True,
            states={
                'confirmed': [('readonly', True)],
                'paid': [('readonly', True)],
                'draft': [('readonly', False)]}),
        'move_id': fields.many2one(
            'account.move', 'VAT statement move', readonly=True),

        'state': fields.selection([
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('paid', 'Paid'),
        ], 'State', readonly=True),

        'payment_term_id': fields.many2one(
            'account.payment.term', 'Payment Term',
            states={'confirmed': [('readonly', True)],
                    'paid': [('readonly', True)],
                    'draft': [('readonly', False)]}),
        'reconciled': fields.function(
            _reconciled, string='Paid/Reconciled', type='boolean',
            store={
                'account.vat.period.end.statement': (
                    lambda self, cr, uid, ids, c={}: ids, None, 50),
                'account.move.line': (_get_statement_from_line, None, 50),
                'account.move.reconcile': (
                    _get_statement_from_reconcile, None, 50),
            }, help="It indicates that the statement has been paid and the "
                    "journal entry of the statement has been reconciled with "
                    "one or several journal entries of payment."),
        'residual': fields.function(
            _amount_residual, digits_compute=dp.get_precision('Account'),
            string='Balance',
            store={
                'account.vat.period.end.statement': (
                    lambda self, cr, uid, ids, c={}: ids,
                    [
                        'debit_vat_account_line_ids',
                        'credit_vat_account_line_ids',
                        'generic_vat_account_line_ids', 'move_id', 'state'
                    ], 50),
                'statement.credit.account.line': (
                    _get_credit_line, ['amount', 'statement_id'], 50),
                'statement.debit.account.line': (
                    _get_debit_line, ['amount', 'statement_id'], 50),
                'statement.generic.account.line': (
                    _get_generic_line, ['amount', 'statement_id'], 50),
                'account.move': (_get_statement_from_move, None, 50),
                'account.move.line': (_get_statement_from_line, None, 50),
                'account.move.reconcile': (
                    _get_statement_from_reconcile, None, 50),
            },
            help="Remaining amount due."),
        'payment_ids': fields.function(
            _compute_lines, relation='account.move.line', type="many2many",
            string='Payments'),
        'period_ids': fields.one2many(
            'account.period', 'vat_statement_id', 'Periods'),
        'interest': fields.boolean('Compute Interest'),
        'interest_percent': fields.float('Interest - Percent'),
        'fiscal_page_base': fields.integer('Last printed page', required=True),
        'company_id': fields.many2one('res.company', 'Company'),

        'vat_settlement_attachment_id': fields.many2one(
            'account.vat.settlement.attachment',
            'VAT Settlement Export File',
            readonly=True),

        'show_zero': fields.boolean('Show zero amount lines'),
        'soggetto_codice_fiscale':
            fields.char(
                'Codice fiscale dichiarante',
                size=16,  # required=True,
                help="CF del soggetto che presenta la comunicazione "
                     "se PF o DI o con la specifica carica"),
        # TODO: use module l10n_it_codici_carica
        'codice_carica': fields.selection([
            ('0', 'Azienda PF (Ditta indivisuale/Professionista/eccetera)'),
            ('1', 'Legale rappresentante, socio amministratore'),
            ('2', 'Rappresentante di minore,interdetto,eccetera'),
            ('3', 'Curatore fallimentare'),
            ('4', 'Commissario liquidatore'),
            ('5', 'Custode giudiziario'),
            ('6', 'Rappresentante fiscale di soggetto non residente'),
            ('7', 'Erede'),
            ('8', 'Liquidatore'),
            ('9', 'Obbligato di soggetto estinto'),
            ('10', 'Rappresentante fiscale art. 44c3 DLgs 331/93'),
            ('11', 'Tutore di minore'),
            ('12', 'Liquidatore di DI'),
            ('13', 'Amministratore di condominio'),
            ('14', 'Pubblica Amministrazione'),
            ('15', 'Commissario PA'), ],
            'Codice carica',
        ),

        'progressivo_telematico': fields.integer('Progressivo telematico', readonly=True),

        'incaricato_trasmissione_codice_fiscale': fields.char(
            'Codice Fiscale Incaricato',
            size=16,
            help="CF intermediario "
                 "che effettua la trasmissione telematica",
            # required=True
        ),

        'incaricato_trasmissione_numero_CAF': fields.integer(
            'Numero CAF intermediario',
            size=5,
            help="Eventuale numero iscrizione albo del C.A.F."
        ),

        'incaricato_trasmissione_data_impegno': fields.date(
            'Data impegno',  # required=True
        ),

        'is_summary_statement': fields.function(
            _is_summary_statement,
            string=_('Summary Statement'),
            type='boolean',
            store={'account.vat.period.end.statement': (lambda self, cr, uid, ids, c={}: ids, ['period_ids'], 50)},
            help=_("It indicates that the statement summarize an entire fiscal year. That happens when the statement refers to an opening/closing periods.")
        )
    }

    _defaults = {
        'authority_partner_id': _get_default_tax_authority,
        'journal_id': _get_default_journal_id,
        'date': fields.date.context_today,
        'interest': _get_default_interest,
        'interest_percent': _get_default_interest_percent,
        'fiscal_page_base': 1,
        'company_id': lambda self, cr, uid, c:
            self.pool.get('res.company')._company_default_get(
                cr, uid, 'account.vat.period.end.statement', context=c),
        'show_zero': False,
    }

    def _get_tax_code_amount(self, cr, uid, tax_code_id, period_id, context):
        if not context:
            context = {}
        context['period_id'] = period_id
        return self.pool.get('account.tax.code').browse(
            cr, uid, tax_code_id, context)._sum_vat_period(
            None, None, context)[tax_code_id]

    def unlink(self, cr, uid, ids, context=None):
        if isinstance(ids, (long, int)):
            ids = [ids]
        for statement in self.browse(cr, uid, ids, context):
            if statement.state == 'confirmed' or statement.state == 'paid':
                raise orm.except_orm(
                    _('Error!'),
                    _('You cannot delete a confirmed or paid statement'))
        res = super(AccountVatPeriodEndStatement, self).unlink(
            cr, uid, ids, context)
        return res

    def copy(self, cr, uid, ids, defaults, context=None):
        if context is None:
            context = self.pool['res.users'].context_get(cr, uid)
        defaults['vat_settlement_attachment_id'] = False
        return super(AccountVatPeriodEndStatement, self).copy(
            cr, uid, ids, defaults, context)

    def statement_draft(self, cr, uid, ids, context=None):
        for statement in self.browse(cr, uid, ids, context):
            if statement.move_id:
                statement.move_id.unlink()
        self.write(cr, uid, ids, {'state': 'draft'})

    def statement_paid(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'paid'})

    def create_move(self, cr, uid, ids, context=None):
        move_obj = self.pool.get('account.move')
        term_pool = self.pool.get('account.payment.term')
        line_obj = self.pool.get('account.move.line')
        period_obj = self.pool.get('account.period')
        for statement in self.browse(cr, uid, ids, context):
            period_ids = period_obj.find(
                cr, uid, dt=statement.date, context=context)
            if len(period_ids) != 1:
                raise orm.except_orm(_('Encoding error'), _(
                    "No period found or more than one period found for the "
                    "given date."))
            move_data = {
                'date': statement.date,
                'journal_id': statement.journal_id.id,
                'period_id': period_ids[0],
            }
            move_id = move_obj.create(cr, uid, move_data)
            statement.write({'move_id': move_id})

            for debit_line in statement.debit_vat_account_line_ids:
                if debit_line.amount != 0.0:
                    debit_vat_data = {
                        'name': _('Debit VAT'),
                        'account_id': debit_line.account_id.id,
                        'move_id': move_id,
                        'journal_id': statement.journal_id.id,
                        'debit': 0.0,
                        'credit': 0.0,
                        'date': statement.date,
                        'period_id': period_ids[0],
                    }

                    if debit_line.amount > 0:
                        debit_vat_data['debit'] = math.fabs(debit_line.amount)
                    else:
                        debit_vat_data['credit'] = math.fabs(debit_line.amount)
                    line_obj.create(cr, uid, debit_vat_data)

            for credit_line in statement.credit_vat_account_line_ids:
                if credit_line.amount != 0.0:
                    credit_vat_data = {
                        'name': _('Credit VAT'),
                        'account_id': credit_line.account_id.id,
                        'move_id': move_id,
                        'journal_id': statement.journal_id.id,
                        'debit': 0.0,
                        'credit': 0.0,
                        'date': statement.date,
                        'period_id': period_ids[0],
                    }
                    if credit_line.amount < 0:
                        credit_vat_data['debit'] = math.fabs(
                            credit_line.amount)
                    else:
                        credit_vat_data['credit'] = math.fabs(
                            credit_line.amount)
                    line_obj.create(cr, uid, credit_vat_data)

            if statement.previous_credit_vat_amount:
                previous_credit_vat_data = {
                    'name': _('Previous Credits VAT'),
                    'account_id': statement.previous_credit_vat_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement.date,
                    'period_id': period_ids[0],
                }
                if statement.previous_credit_vat_amount < 0:
                    previous_credit_vat_data['debit'] = math.fabs(
                        statement.previous_credit_vat_amount)
                else:
                    previous_credit_vat_data['credit'] = math.fabs(
                        statement.previous_credit_vat_amount)
                line_obj.create(cr, uid, previous_credit_vat_data)

            if statement.previous_debit_vat_amount:
                previous_debit_vat_data = {
                    'name': _('Previous Debits VAT'),
                    'account_id': statement.previous_debit_vat_account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement.date,
                    'period_id': period_ids[0],
                }
                if statement.previous_debit_vat_amount > 0:
                    previous_debit_vat_data['debit'] = math.fabs(
                        statement.previous_debit_vat_amount)
                else:
                    previous_debit_vat_data['credit'] = math.fabs(
                        statement.previous_debit_vat_amount)
                line_obj.create(cr, uid, previous_debit_vat_data)

            for generic_line in statement.generic_vat_account_line_ids:
                generic_vat_data = {
                    'name': _('Other VAT Credits / Debits'),
                    'account_id': generic_line.account_id.id,
                    'move_id': move_id,
                    'journal_id': statement.journal_id.id,
                    'debit': 0.0,
                    'credit': 0.0,
                    'date': statement.date,
                    'period_id': period_ids[0],
                }
                if generic_line.amount < 0:
                    generic_vat_data['debit'] = math.fabs(generic_line.amount)
                else:
                    generic_vat_data['credit'] = math.fabs(generic_line.amount)
                line_obj.create(cr, uid, generic_vat_data)

            end_debit_vat_data = {
                'name': _('Tax Authority VAT'),
                'account_id': statement.authority_vat_account_id.id,
                'partner_id': statement.authority_partner_id.id,
                'move_id': move_id,
                'journal_id': statement.journal_id.id,
                'date': statement.date,
                'period_id': period_ids[0],
            }
            if statement.authority_vat_amount > 0:
                end_debit_vat_data['debit'] = 0.0
                end_debit_vat_data['credit'] = math.fabs(
                    statement.authority_vat_amount)
                if statement.payment_term_id:
                    due_list = term_pool.compute(
                        cr, uid, statement.payment_term_id.id, math.fabs(
                            statement.authority_vat_amount),
                        date_ref=statement.date, context=context)
                    if len(due_list) == 0:
                        raise orm.except_orm(
                            _('Error'),
                            _('The payment term %s does not have due dates')
                            % statement.payment_term_id.name)
                    for term in due_list:
                        current_line = end_debit_vat_data
                        current_line['credit'] = term[1]
                        current_line['date_maturity'] = term[0]
                        line_obj.create(cr, uid, current_line)
                else:
                    line_obj.create(cr, uid, end_debit_vat_data)
            elif statement.authority_vat_amount < 0:
                end_debit_vat_data['debit'] = math.fabs(
                    statement.authority_vat_amount)
                end_debit_vat_data['credit'] = 0.0
                line_obj.create(cr, uid, end_debit_vat_data)

            move = move_obj.browse(cr, uid, move_id, context=context)
            if move.journal_id.entry_posted:
                move_obj.post(cr, uid, [move_id], context=context)

            self.write(cr, uid, statement.id, {'state': 'confirmed'})

        return True

    def build_tax_tree(self, cr, uid, company_id, context=None):
        """[antoniov: 2017-06-03]
        account.tax.code records cannot be recognized as VAT or base amount and
        Italian law requires to couple base and VAT amounts,
        thats is stored on account.tax model.
        This function rebuilds (base,VAT) couples throught account.tax.
        Warning: end-user could have set many-2-many base,VAT relationship;
        in this case some couple (base,VAT) may be wrong.
        However, all tutorial of Odoo Italian Comunity and standard Italian
        Localization have just one-2-one relationshiop on (base,VAT).
        return: tax_tree[type][basevat][left], where
        - type may be 'sale', 'purchase' or 'all'
        - basevat may be 'tax_code_id', 'base_code_id', 'ref_tax_code_id' or
              'ref_base_code_id'
        - left is id of account.tax.code record
        """
        # todo test with partial deductible taxes!
        context = {} if context is None else context
        tax_pool = self.pool.get('account.tax')
        tax_ids = tax_pool.search(cr, uid, [('company_id', '=', company_id)])
        tax_tree = {}
        for tax_id in tax_ids:
            tax = tax_pool.browse(cr, uid, tax_id)
            type = tax.type_tax_use

            if type not in tax_tree:
                tax_tree[type] = {}

            for basevat in ('tax_code_id', 'base_code_id', 'ref_tax_code_id', 'ref_base_code_id'):
                if basevat[-11:] == 'tax_code_id':
                    vatbase = basevat[0:-11] + 'base_code_id'
                elif basevat[-12:] == 'base_code_id':
                    vatbase = basevat[0:-12] + 'tax_code_id'
                else:
                    vatbase = False             # never should run here!

                if basevat not in tax_tree[type]:
                    tax_tree[type][basevat] = {}

                if getattr(tax, basevat):
                    left = getattr(tax, basevat).id
                    if getattr(tax, vatbase):
                        right = getattr(tax, vatbase).id
                        tax_tree[type][basevat][left] = right
                    elif tax.parent_id and getattr(tax.parent_id, vatbase):
                        right = getattr(tax.parent_id, vatbase).id
                        tax_tree[type][basevat][left] = right
                    elif left not in tax_tree[type][basevat]:
                        tax_tree[type][basevat][left] = False

                elif tax.parent_id and getattr(tax.parent_id, basevat):
                    left = getattr(tax.parent_id, basevat).id
                    if getattr(tax, vatbase):
                        right = getattr(tax, vatbase).id
                        tax_tree[type][basevat][left] = right

        return tax_tree

    def compute_amount_dbt_crd(self, cr, uid, statement, company_id, tax_tree, show_zero=None, context=None):
        context = {} if context is None else context

        if show_zero is None:
            show_zero = statement.show_zero

        tax_pool = self.pool.get('account.tax')
        tax_code_pool = self.pool.get('account.tax.code')

        dbt_crd_line_ids = []
        dbt_crd_tax_code_ids = tax_code_pool.search(cr, uid, [
            ('exclude_from_registries', '=', False),
            ('company_id', '=', company_id),
        ], context=context)

        for dbt_crd_tax_code_id in dbt_crd_tax_code_ids:

            if tax_code_pool.search(cr, uid, [('parent_id', '=', dbt_crd_tax_code_id)]):
                continue

            dbt_crd_tax_code = tax_code_pool.browse(cr, uid, dbt_crd_tax_code_id, context)

            is_nondeductible = False

            # check if the tax code is used into a parent tax
            is_parent_tax = False
            parent_tax_domain = [
                '|', ('base_code_id', '=', dbt_crd_tax_code_id), ('ref_base_code_id', '=', dbt_crd_tax_code_id),
                '|', ('tax_code_id', '=', False), ('ref_tax_code_id', '=', False)
            ]
            parent_tax_ids = tax_pool.search(cr, uid, parent_tax_domain, context=context)
            parent_tax = tax_pool.browse(cr, uid, parent_tax_ids, context=context)
            # assuming that one account.tax.code is used only in one account.tax
            if len(parent_tax) > 1:
                _logger.warning(parent_tax)
                raise orm.except_orm(_('Warning!'), _('Tax code %s is used for many taxes!') % dbt_crd_tax_code.name)

            if parent_tax:
                is_parent_tax = True
                is_nondeductible = parent_tax.nondeductible

            # check if the tax code is used into a child tax
            is_child_tax = False
            child_tax_domain = [
                '|', ('tax_code_id', '=', dbt_crd_tax_code_id), ('ref_tax_code_id', '=', dbt_crd_tax_code_id),
                '|', ('base_code_id', '=', False), ('ref_base_code_id', '=', False)
            ]
            child_tax_ids = tax_pool.search(cr, uid, child_tax_domain, context=context)
            child_tax = tax_pool.browse(cr, uid, child_tax_ids, context=context)
            # assuming that one account.tax.code is used only in two account.tax that are child of the same parent tax
            if len(child_tax) > 2 or len(child_tax.mapped('parent_id')) > 1:
                raise orm.except_orm(_('Warning!'), _('Tax code %s is used for many taxes!') % dbt_crd_tax_code.name)

            if child_tax:
                is_child_tax = True
                is_nondeductible = child_tax.mapped('nondeductible')[0]

            period_ids_to_evaluate = []
            for period in statement.period_ids:
                if period.special:
                    fy_period_ids = period.fiscalyear_id.period_ids.filtered(lambda p: not p.special).ids
                    period_ids_to_evaluate += fy_period_ids
                else:
                    period_ids_to_evaluate.append(period.id)

            total = 0.0
            for period_id in period_ids_to_evaluate:
                ctx = context.copy()
                ctx['period_id'] = period_id
                total += tax_code_pool.browse(cr, uid, dbt_crd_tax_code_id, ctx).sum_vat_period

            if not statement.show_zero and total == 0.0:
                continue

            left_id = right_id = False
            for type in tax_tree:
                for basevat in ('tax_code_id', 'base_code_id', 'ref_tax_code_id', 'ref_base_code_id'):
                    if basevat[-11:] == 'tax_code_id':
                        basevat_id = basevat[-11:]
                        vatbase = basevat[0:-11] + 'base_code_id'
                        vatbase_id = vatbase[-12:]
                    elif basevat[-12:] == 'base_code_id':
                        basevat_id = basevat[-12:]
                        vatbase = basevat[0:-12] + 'tax_code_id'
                        vatbase_id = vatbase[-11:]
                    else:
                        vatbase_id = False             # never should run here!

                    if dbt_crd_tax_code_id in tax_tree[type][basevat]:
                        left_id = dbt_crd_tax_code_id
                        if left_id in tax_tree[type][basevat]:
                            right_id = tax_tree[type][basevat][left_id]
                        else:
                            right_id = False

                        if type == 'sale':
                            dbt_crd = 'debit'
                        elif type == 'purchase':
                            dbt_crd = 'credit'
                        else:
                            dbt_crd = dbt_crd_tax_code.vat_statement_type

                        if left_id and right_id:
                            break

                if left_id and right_id:
                    break

            if not left_id and not right_id:
                continue

            if (is_child_tax or is_parent_tax) and is_nondeductible:
                basevat_id_field = 'non_deductible_' + basevat_id
                vatbase_id_field = 'non_deductible_' + vatbase_id
                base_amount_field = 'non_deductible_base_amount'
                amount_field = 'non_deductible_amount'
            else:
                basevat_id_field = basevat_id
                vatbase_id_field = vatbase_id
                base_amount_field = 'base_amount'
                amount_field = 'amount'

            found_rec = False
            for id, rec in enumerate(dbt_crd_line_ids):
                if dbt_crd == rec['dbt_crd']:
                    if (basevat_id_field in rec and rec[basevat_id_field] == left_id) or (basevat_id in rec and rec[basevat_id] == left_id):
                        found_rec = True
                        break
                    elif (vatbase_id_field in rec and rec[vatbase_id_field] == right_id) or (vatbase_id in rec and rec[vatbase_id] == right_id):
                        found_rec = True
                        break

            if not found_rec:
                rec = {}
                rec['dbt_crd'] = dbt_crd

            if dbt_crd_tax_code.vat_statement_account_id:
                rec['account_id'] = dbt_crd_tax_code.vat_statement_account_id.id

            if basevat_id == 'tax_code_id':
                # if is_child_tax or is_parent_tax:
                #     basevat_id = 'non_deductible_' + basevat_id

                rec[basevat_id_field] = left_id
                rec[amount_field] = total * dbt_crd_tax_code.vat_statement_sign

                if right_id:
                    if vatbase_id_field not in rec:
                        # if is_child_tax or is_parent_tax:
                        #     vatbase_id = 'non_deductible_' + vatbase_id

                        rec[vatbase_id_field] = right_id

                    if base_amount_field not in rec:
                        rec[base_amount_field] = 0.0

            elif basevat_id == 'base_code_id':
                # if is_child_tax or is_parent_tax:
                #     basevat_id = 'non_deductible_' + basevat_id

                rec[basevat_id_field] = left_id
                rec[base_amount_field] = total * dbt_crd_tax_code.vat_statement_sign

                if right_id:
                    if vatbase_id_field not in rec:
                        # if is_child_tax or is_parent_tax:
                        #     vatbase_id = 'non_deductible_' + vatbase_id

                        rec[vatbase_id_field] = right_id

                    if amount_field not in rec:
                        rec[amount_field] = 0.0

            if found_rec:
                del dbt_crd_line_ids[id]
            dbt_crd_line_ids.append(rec)

        id = 0
        while id < len(dbt_crd_line_ids):
            if not show_zero and rec.get(amount_field, 0) == 0 and rec.get(base_amount_field, 0) == 0:
                del dbt_crd_line_ids[id]
            else:
                id += 1

        return dbt_crd_line_ids

    def compute_amounts(self, cr, uid, ids, context=None):
        context = {} if context is None else context
        company_id = self.pool.get('res.users').browse(cr, uid, uid, context).company_id.id

        debit_line_pool = self.pool.get('statement.debit.account.line')
        credit_line_pool = self.pool.get('statement.credit.account.line')
        statement_generic_account_line_obj = self.pool['statement.generic.account.line']
        decimal_precision_obj = self.pool['decimal.precision']

        tax_tree = self.build_tax_tree(cr, uid, company_id, context)
        for statement in self.browse(cr, uid, ids, context):
            company_id = statement.company_id.id
            statement.write({'previous_debit_vat_amount': 0.0})
            prev_statement_ids = self.search(cr, uid, [('date', '<', statement.date)], order='date')

            if prev_statement_ids:
                prev_statement = self.browse(cr, uid, prev_statement_ids[len(prev_statement_ids) - 1], context)

                if prev_statement.residual > 0 and prev_statement.authority_vat_amount > 0:
                    statement.write({'previous_debit_vat_amount': prev_statement.residual})
                elif prev_statement.authority_vat_amount < 0:
                    statement.write({'previous_credit_vat_amount': -prev_statement.authority_vat_amount})

            dbt_crd_ids = self.compute_amount_dbt_crd(cr, uid, statement, company_id, tax_tree, context)

            credit_line_ids = []
            debit_line_ids = []
            for rec in dbt_crd_ids:
                if rec['dbt_crd'] == 'debit':
                    del rec['dbt_crd']
                    debit_line_ids.append(rec)
                elif rec['dbt_crd'] == 'credit':
                    del rec['dbt_crd']
                    credit_line_ids.append(rec)

            for debit_line in statement.debit_vat_account_line_ids:
                debit_line.unlink()
            for credit_line in statement.credit_vat_account_line_ids:
                credit_line.unlink()
            for debit_vals in debit_line_ids:
                debit_vals.update({'statement_id': statement.id})
                debit_line_pool.create(cr, uid, debit_vals, context=context)
            for credit_vals in credit_line_ids:
                credit_vals.update({'statement_id': statement.id})
                credit_line_pool.create(cr, uid, credit_vals, context=context)

            interest_amount = 0.0
            # if exits Delete line with interest
            acc_id = self.get_account_interest(cr, uid, ids, context)

            domain = [('account_id', '=', acc_id), ('statement_id', '=', statement.id)]
            line_ids = statement_generic_account_line_obj.search(cr, uid, domain)

            if line_ids:
                statement_generic_account_line_obj.unlink(cr, uid, line_ids)

            # Compute interest
            if statement.interest and statement.authority_vat_amount > 0:
                interest_amount = (-1 * round(
                    statement.authority_vat_amount *
                    (float(statement.interest_percent) / 100),
                    decimal_precision_obj.precision_get(cr, uid, 'Account')))

            # Add line with interest
            if interest_amount:
                val = {
                    'statement_id': statement.id,
                    'account_id': acc_id,
                    'amount': interest_amount,
                }
                statement_generic_account_line_obj.create(cr, uid, val)

            # update authority account
            if statement.authority_vat_amount <= 0:
                account_id = statement.company_id.of_account_end_vat_statement_credit_account_id.id
            else:
                account_id = statement.company_id.of_account_end_vat_statement_debit_account_id.id

            statement.write({'authority_vat_account_id': account_id})

        return True

    def confirm_summary_statement(self, cr, uid, ids, context=None):
        context = context or {}
        statements = self.browse(cr, uid, ids, context=context)
        for statement in statements:
            if not statement.is_summary_statement:
                raise orm.except_orm(
                    _('Wrong Statement configuration!'),
                    _("Cannot confirm a statement as summary when does not have any opening/closing period!")
                )

        self.write(cr, uid, ids, {'state': 'confirmed'}, context=context)
        return True

    def on_change_partner_id(self, cr, uid, ids, partner_id, context=None):
        partner = self.pool.get('res.partner').browse(
            cr, uid, partner_id, context)
        return {
            'value': {
                'authority_vat_account_id': partner.property_account_payable.id
            }
        }

    def onchange_interest(self, cr, uid, ids, interest, context=None):
        res = {}
        if not ids:
            return res
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        company = user.company_id

        res = {'value': {
            'interest_percent':
                company.of_account_end_vat_statement_interest_percent,
        }}
        return res

    def onchange_fiscalcode(self, cr, uid, ids, fiscalcode, name, context=None):
        if fiscalcode:
            if len(fiscalcode) == 11:
                res_partner_pool = self.pool.get('res.partner')
                chk = res_partner_pool.simple_vat_check(cr, uid, 'it', fiscalcode)
                if not chk:
                    return {
                        'value': {name: False},
                        'warning': {
                            'title': 'Invalid fiscalcode!',
                            'message': 'Invalid vat number'
                        }
                    }
            elif len(fiscalcode) != 16:
                return {
                    'value': {name: False},
                    'warning': {
                        'title': 'Invalid len!',
                        'message': 'Fiscal code len must be 11 or 16'
                    }
                }
            else:
                chk = codicefiscale.control_code(fiscalcode[0:15])
                if chk != fiscalcode[15]:
                    value = fiscalcode[0:15] + chk
                    return {
                        'value': {name: value},
                        'warning': {
                            'title': 'Invalid fiscalcode!',
                            'message': 'Fiscal code could be %s' % (value)
                        }
                    }
            return {'value': {name: fiscalcode}}
        return {}

    def get_account_interest(self, cr, uid, ids, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        company = user.company_id
        if (
            company.of_account_end_vat_statement_interest or
            any([s.interest for s in self.browse(cr, uid, ids, context)])
        ):
            if not company.of_account_end_vat_statement_interest_account_id:
                raise orm.except_orm(
                    _('Error VAT Configuration!'),
                    _("The account for vat interest must be configurated"))

        return company.of_account_end_vat_statement_interest_account_id.id

    def action_cancel(self, cr, uid, ids, context=None):
        for vat_statement in self.browse(cr, uid, ids, context):
            if vat_statement:
                raise orm.except_orm(
                    _('Error!'),
                    _('You should delete VAT Settlement before'
                      ' deleting Vat Period End Statement')
                )
        return super(AccountVatPeriodEndStatement, self).action_cancel(
            cr, uid, ids, context)


# TODO: SEPARATE IN OTHER FILES
from openerp import models, fields, api, _


class StatementDebitAccountLine(models.Model):
    _name = 'statement.debit.account.line'

    statement_id = fields.Many2one(
        comodel_name='account.vat.period.end.statement',
        string=_('VAT statement')
    )

    account_id = fields.Many2one(
        comodel_name='account.account',
        string=_('Account')
    )

    base_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string=_('Base Tax Code')
    )

    base_amount = fields.Float(
        string=_('Base amount'),
        digits_compute=dp.get_precision('Account')
    )

    tax_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string=_('Tax Code'),
        help=_('The deductible Tax Code')
    )

    amount = fields.Float(
        string=_('Amount'),
        digits_compute=dp.get_precision('Account'),
        help=_('The deductible tax amount, used to compute the total authority vat amount.')
    )

    non_deductible_base_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string=_('Non Deductible Base Code'),
        help=_('The non deductible Base Tax Code')
    )

    non_deductible_base_amount = fields.Float(
        string=_('Non Deductible Base Amount'),
        digits_compute=dp.get_precision('Account'),
        help=_('The non deductible base tax amount, used in the tax authority end vat statement.')
    )

    non_deductible_tax_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string=_('Non Deductible Tax Code'),
        help=_('The non deductible Tax Code')
    )

    non_deductible_amount = fields.Float(
        string=_('Non Deductible Amount'),
        digits_compute=dp.get_precision('Account'),
        help=_('The non deductible tax amount, used in the tax authority end vat statement.')
    )

    @api.multi
    def show_vat_statement_account_move_lines(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        act_window = self.env['ir.actions.act_window']
        module_name = 'account'
        action_name = 'action_tax_code_line_open'

        tree_view_name = 'account_vat_period_end_statement_account_move_line_tree_view'
        tree_view = ir_model_data.get_object_reference('account_vat_period_end_statement', tree_view_name)

        action_data = ir_model_data.get_object_reference(module_name, action_name)
        action_id = action_data and action_data[1] or False
        result = act_window.browse(action_id).read()[0]

        result['views'] = [(tree_view and tree_view[1] or False, 'tree')]

        result['domain'] = [
            ('tax_code_id', 'child_of', [self.tax_code_id.id, self.base_code_id.id]),
            ('move_id.state', '!=', 'draft'),
            ('vat_period_id', 'in', self.statement_id.period_ids.ids)
        ]

        result['context'] = {'search_default_group_by_tax_code_id': 1}
        return result


class StatementCreditAccountLine(models.Model):
    _name = 'statement.credit.account.line'

    statement_id = fields.Many2one(
        comodel_name='account.vat.period.end.statement',
        string=_('VAT statement')
    )

    account_id = fields.Many2one(
        comodel_name='account.account',
        string=_('Account')
    )

    base_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string=_('Base Tax Code')
    )

    base_amount = fields.Float(
        string=_('Base amount'),
        digits_compute=dp.get_precision('Account')
    )

    tax_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string=_('Tax Code'),
        help=_('The deductible Tax Code')
    )

    amount = fields.Float(
        string=_('Amount'),
        digits_compute=dp.get_precision('Account'),
        help=_('The deductible tax amount, used to compute the total authority vat amount.')
    )

    non_deductible_base_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string=_('Non Deductible Base Code'),
        help=_('The non deductible Base Code')
    )

    non_deductible_base_amount = fields.Float(
        string=_('Non Deductible Base Amount'),
        digits_compute=dp.get_precision('Account'),
        help=_('The non deductible base tax amount, used in the tax authority end vat statement.')
    )

    non_deductible_tax_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string=_('Non Deductible Tax Code'),
        help=_('The non deductible Tax Code')
    )

    non_deductible_amount = fields.Float(
        string=_('Non Deductible Amount'),
        digits_compute=dp.get_precision('Account'),
        help=_('The non deductible tax amount, used in the tax authority end vat statement.')
    )

    @api.multi
    def show_vat_statement_account_move_lines(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        act_window = self.env['ir.actions.act_window']
        module_name = 'account'
        action_name = 'action_tax_code_line_open'

        tree_view_name = 'account_vat_period_end_statement_account_move_line_tree_view'
        tree_view = ir_model_data.get_object_reference('account_vat_period_end_statement', tree_view_name)

        action_data = ir_model_data.get_object_reference(module_name, action_name)
        action_id = action_data and action_data[1] or False
        result = act_window.browse(action_id).read()[0]

        result['views'] = [(tree_view and tree_view[1] or False, 'tree')]

        result['domain'] = [
            ('tax_code_id', 'child_of', [self.tax_code_id.id, self.base_code_id.id]),
            ('move_id.state', '!=', 'draft'),
            ('vat_period_id', 'in', self.statement_id.period_ids.ids)
        ]

        result['context'] = {'search_default_group_by_tax_code_id': 1}
        return result


class StatementGenericAccountLine(models.Model):
    _name = 'statement.generic.account.line'

    statement_id = fields.Many2one(
        comodel_name='account.vat.period.end.statement',
        string=_('VAT statement')
    )

    account_id = fields.Many2one(
        comodel_name='account.account',
        string=_('Account')
    )

    base_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string=_('Base Tax Code')
    )

    base_amount = fields.Float(
        string=_('Base amount'),
        digits_compute=dp.get_precision('Account')
    )

    tax_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string=_('Tax Code'),
        help=_('The deductible Tax Code')
    )

    amount = fields.Float(
        string=_('Amount'),
        digits_compute=dp.get_precision('Account'),
        help=_('The deductible tax amount, used to compute the total authority vat amount.')
    )

    non_deductible_base_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string=_('Non Deductible Base Code'),
        help=_('The non deductible Base Code')
    )

    non_deductible_base_amount = fields.Float(
        string=_('Non Deductible Base Amount'),
        digits_compute=dp.get_precision('Account'),
        help=_('The non deductible base tax amount, used in the tax authority end vat statement.')
    )

    non_deductible_tax_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string=_('Non Deductible Tax Code'),
        help=_('The non deductible Tax Code')
    )

    non_deductible_amount = fields.Float(
        string=_('Non Deductible Amount'),
        digits_compute=dp.get_precision('Account'),
        help=_('The non deductible tax amount, used in the tax authority end vat statement.')
    )

    @api.one
    @api.onchange('account_id')
    def onchange_vat_account_id(self):
        if self.account_id:
            self.amount = self.account_id.balance


class AccountTaxCode(models.Model):
    _inherit = "account.tax.code"

    vat_statement_account_id = fields.Many2one(
        comodel_name='account.account',
        string=_('Account used for VAT statement'),
        help=_('Set VAT account to compute VAT amount. Please, leave empty if no VAT amount record')
    )

    vat_statement_type = fields.Selection(
        selection=[
            ('credit', 'Credit'),
            ('debit', 'Debit')
        ],
        string=_('Type'),
        default='debit',
        help=_('This establish whether amount will be loaded as debit or credit')
    )

    vat_statement_sign = fields.Integer(
        string=_('Sign used in statement'),
        default=1,
        help=_('If tax code period sum is usually negative, set "-1" here')
    )


class AccountPeriod(models.Model):
    _inherit = "account.period"

    vat_statement_id = fields.Many2one(
        comodel_name='account.vat.period.end.statement',
        string=_('VAT statement')
    )


class AccountVatSettlementAttachment(models.Model):
    _name = "account.vat.settlement.attachment"
    _description = "Vat Settlement Export File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']

    ir_attachment_id = fields.Many2one(
        'ir.attachment',
        _('Attachment'),
        required=True,
        ondelete="cascade"
    )

    vat_statement_ids = fields.One2many(
        comodel_name='account.vat.period.end.statement',
        inverse_name='vat_settlement_attachment_id',
        string=_('VAT Statements'),
        readonly=True
    )
