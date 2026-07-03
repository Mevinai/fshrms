# Copyright (c) 2026, Mesfin Tsegaye and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MyTodo(Document):

    def validate(self):
        if not self.title:
            frappe.msgprint("Title is required", alert=True)
            # frappe.throw("Title is required")

        # Get the logged in user's ID (email)
        # current_user = frappe.session.user

        # Get the full name
        # full_name = frappe.db.get_value("User", current_user, "full_name")

        # Get user roles (returns a list)
        # user_roles = frappe.get_roles(current_user)

        # frappe.throw(f"Current User: {current_user}, Full Name: {full_name}, Roles: {user_roles}")

        # customers=frappe.get_all(
        #       "Customer",      
        #     #    filters={"status": "Active"},      
        #        fields=["name","customer_name"] 
        #     )
        # frappe.throw(f"Active Customers: {customers}")

        # customer_info = frappe.db.get_value(
        #     "Customer", 
        #     "Palmer Productions Ltd.", 
        #     ["customer_name", "territory"], 
        #     as_dict=True
        # )

        # frappe.throw(f"Active Customers: {customer_info}")


        # doc = frappe.get_doc({
        # 'doctype': 'My Todo',
        # 'title': 'New Task'
        # })
        # doc.insert()

        # Fetch specific fields for a condition
        # documents = frappe.db.sql("""
        #     SELECT name, customer_name, grand_total 
        #     FROM `tabSales Invoice`
        #     WHERE docstatus = 1 AND grand_total > %(amount)s
        # """, {"amount": 5000}, as_dict=True)

        # frappe.throw(f"Documents: {documents}")

        # for doc in documents:
        #     print(doc.name, doc.customer_name)


        # if not self.description:
        #     self.description = "Default description"
        
        # pi_id=self.purchase_invoice
        # pi=frappe.get_doc("Purchase Invoice",pi_id)
        # doc=frappe.get_doc("My Todo",self.name)

        # items=pi.items
        # for item in items:
        #     doc.append(
        #     "items",
        #     {
        #     "item":item.item_code,
        #     "amount":item.rate,
        #     "tax":item.item_tax_amount
        #     }
        # )
        # self.items=doc.items
        # self.customer_name=customer_info.customer_name
        # frappe.throw(f"Description is required. {w_items[0]}")

    # def before_save(self):
    #     # runs just before save
    #     self.title = self.title.strip().title()

    # def after_insert(self):
    #     # runs only once after new record is created
    #     frappe.logger().info(f"MyTodo created: {self.name}")

    # def on_update(self):
    #     # runs every time record is updated
    #     frappe.logger().info(f"MyTodo updated: {self.name}")

    # def before_submit(self):
    #     # if your DocType is submittable
    #     frappe.logger().info("About to submit MyTodo")