import frappe

def get_context(context):
    items=frappe.get_all("Item",fields=["name","item_name","standard_rate","image"])
    context.items=items