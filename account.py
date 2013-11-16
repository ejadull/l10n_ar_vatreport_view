from openerp.osv import fields,osv
from openerp import tools
 
class account_invoice(osv.osv):
    _name = "account.tax.vat_report"
    _description = "VAT Report"
    _auto = False
    _columns = {
	'journal_name': fields.char('Journal Name',size=128,readonly=True),
	'invoice_number': fields.char('Invoice Number',size=32,readonly=True),
	'account_name': fields.char('Account Name',size=128,readonly=True),
	'tax_name': fields.char('Tax Name',size=128,readonly=True),
	'partner_name': fields.char('Partner Name',size=128,readonly=True),
	'document_type_name': fields.char('Doc Type',size=64,readonly=True),
	'document_number': fields.char('Doc Number',size=32,readonly=True),
	'responsability_name': fields.char('Resp Name',size=32,readonly=True),
	'base_amount': fields.float('Base Amount',readonly=True),
	'tax_amount': fields.float('Tax Amount',readonly=True),
	'amount': fields.float('Amount',readonly=True),
	}
 
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'account_tax_vat_report')
	cr.execute("""
		create or replace view account_tax_vat_report as (
		select a.id as id,d.name as journal_name,c.number as invoice_number,b.name as account_name,h.description as tax_name,
			e.name as partner_name,f.name as document_type_name,e.document_number as document_number,
			g.name as responsability_name,
			a.base_amount as base_amount, a.tax_amount as tax_amount, a.amount as amount
			from account_invoice_tax a
				inner join account_account b on a.account_id = b.id
				inner join account_invoice c on a.invoice_id = c.id
				inner join account_journal d on c.journal_id = d.id
				inner join res_partner e on c.partner_id = e.id
				inner join afip_document_type f on e.document_type_id = f.id
				inner join afip_responsability g on e.responsability_id = g.id
				inner join account_tax h on a.tax_code_id = h.tax_code_id
				)
	""")	
        #cr.execute("""
        #    CREATE OR REPLACE VIEW my_report_model AS (
        #        SELECT cbl.analytic_account_id AS id,
        #            aaap.name AS parent_name,
        #            aaa.name AS child_name,
        #            cbl.date_from,
        #            cbl.date_to,
        #            cbl.planned_amount
        #        FROM crossovered_budget_lines cbl
        #        INNER JOIN account_analytic_account aaa ON cbl.analytic_account_id = aaa.id
        #        LEFT OUTER JOIN account_analytic_account aaap ON aaa.parent_id = aaap.id
        #    )
        #""")
 
account_invoice()
