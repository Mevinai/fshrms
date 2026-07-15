

import frappe

@frappe.whitelist(allow_guest=False)
def get_purchase_invoice():
    return "TEST"
