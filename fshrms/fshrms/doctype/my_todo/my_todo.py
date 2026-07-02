# Copyright (c) 2026, Mesfin Tsegaye and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MyTodo(Document):

    def validate(self):
        # runs before saving (insert/update)
        if not self.description:
            frappe.throw("Description is required")

    def before_save(self):
        # runs just before save
        self.title = self.title.strip().title()

    def after_insert(self):
        # runs only once after new record is created
        frappe.logger().info(f"MyTodo created: {self.name}")

    def on_update(self):
        # runs every time record is updated
        frappe.logger().info(f"MyTodo updated: {self.name}")

    def before_submit(self):
        # if your DocType is submittable
        frappe.logger().info("About to submit MyTodo")