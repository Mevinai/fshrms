
import frappe 

def calculate_fdre_income_tax(doc, method):
    print(doc.as_dict())
    frappe.throw(f"This method is deprecated. Please use the new income tax calculation method.")