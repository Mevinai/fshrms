import frappe
from frappe.utils import get_url
import requests
from fshrms.schema.validator import ItemCreateSchema


@frappe.whitelist(allow_guest=True)
def login(username=None, password=None):

    base_url=get_url()
    login_url=f"{base_url}/api/method/login"

    res=requests.post(login_url, data={"usr": username, "pwd": password})

    if res.status_code != 200:
       frappe.throw("Invalid credentials")
    else:
        # Extract Session id
        cookies = res.headers.get("Set-Cookie", "")
        sid=None

        sid=None
        for part in cookies.split(";"):
            if part.strip().startswith("sid="):
                sid = part.strip().split("=")[1]
                if not sid:
                    frappe.throw("Login succeeded but could not get session ID")
        return  sid


#  CUSTOM API ENDPOINTS

# 1. Document API -> Custom Doctype manipautaion
# 2. Doc Events -> Hooks.py 
# 3. REST API
# 4. Monkey Patch
# 5. Deploymnet 


@frappe.whitelist()
def items():
    # result=frappe.get_all("Item",fields=["name","item_Code","creation"])

    si=frappe.get_all("Sales Invoice",fields=["*"])

    si_doc=frappe.get_doc("Sales Invoice", si[0].name)

    items=[]

    for item in si_doc.items:
       items.append(item)

    return items


@frappe.whitelist(allow_guest=False)
def create_item(payload):

    data= ItemCreateSchema(**payload)

    try:
        doc=frappe.get_doc(
        {
         "doctype":"Item",

         "item_code": data.item_code,
         "item_name": data.item_name,
         "item_group": data.item_group,
         "stock_uom": data.stock_uom,
         "is_stock_item": data.is_stock_item,
         "standard_rate": data.standard_rate,
         "item_tax_template": data.item_tax_template,
         "item_prices": data.item_prices
         }
        )

        doc.insert()
        
        return doc.name


    except Exception as e:
        frappe.throw(str(e))

    return data
      



