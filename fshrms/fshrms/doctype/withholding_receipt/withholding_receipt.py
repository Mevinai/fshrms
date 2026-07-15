# Copyright (c) 2026, Mesfin Tsegaye and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WithholdingReceipt(Document):
    
	def validate(self):

		pi= frappe.get_doc("Purchase Invoice",self.purchase_invoice)

		supplier= pi.supplier 
		self.vendor= supplier

		total= pi.total 
		self.total= total or 0
		
		pretax_amount= (total/(1.15))
		vat= pretax_amount * 0.15
		
		if pretax_amount > 20000 and self.tin_trn:
			self.pretax_amount=pretax_amount or 0

			tw_amount= pretax_amount * 0.03
			self.withholding_amount=tw_amount
		else:
			tw_amount= pretax_amount * 0.30
			self.withholding_amount=tw_amount





