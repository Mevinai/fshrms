

import frappe
from fshrms.utils.todo_schema import  ItemCreateSchema
import requests
from frappe.utils import get_url
from pydantic import ValidationError

@frappe.whitelist(allow_guest=True)
def login(username:str,password:str):
    base_url=get_url()
    login_url = f"{base_url}/api/method/login"
    res = requests.post(login_url, data={"usr": username, "pwd": password})
    if res.status_code !=200:
        frappe.throw("Invalid credentials")
    else:
        # Extract session ID (sid) from Set-Cookie header
        cookies = res.headers.get("Set-Cookie", "")
        sid=None
        for part in cookies.split(";"):
            if part.strip().startswith("sid="):
                sid = part.strip().split("=")[1]
                if not sid:
                    frappe.throw("Login succeeded but could not get session ID")
        return  res.json(), sid


@frappe.whitelist(allow_guest=False)
def items():
    cookie = frappe.get_request_header("Cookie")

    if not cookie:
        frappe.throw(("Missing cookie in request header"))
    
    items = frappe.get_all("Item")
    return items


@frappe.whitelist(allow_guest=False)
def item(item_code):
    cookie = frappe.get_request_header("Cookie")

    if not cookie:
        frappe.throw(("Missing cookie in request header"))
    
    item = frappe.get_doc("Item", item_code)
    return item


#  CUSTOM API ENDPOINTS

@frappe.whitelist()
def create_item(payload):

    data = ItemCreateSchema(**payload)

    doc = frappe.get_doc(
        {
            "doctype": "Item",
            "item_code": data.item_code,
            "item_name": data.item_name,
            "item_group": data.item_group,
            "stock_uom": data.stock_uom,
            "is_stock_item": data.is_stock_item,
            "standard_rate": data.standard_rate,
            "item_tax_template": data.item_tax_template,
        }
    )

    doc.insert()
    return doc

