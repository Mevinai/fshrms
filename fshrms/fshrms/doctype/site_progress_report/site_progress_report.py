# Copyright (c) 2026, Mesfin Tsegaye and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests 



class SiteProgressReport(Document):


	# def before_save(self):
	# 	project_id=self.project
	# 	project_doc=frappe.get_doc("Project", project_id)

	# 	project=frappe.get_all(
    #           "Project",      
    #            filters={"name": project_id},      
    #            fields=["name","status","docstatus","project_type"] 
    #         )


	def validate(self):
		if self.progress_percentage is None:
			frappe.throw("Progress percentage cannot be empty.")

		if self.progress_percentage <0 or self.progress_percentage > 100:
			frappe.throw("Progress percentage must be between 0 and 100.",
				title="Invalid Progress Percentage")
			
	# def before_save(self):
	# 	manager=self.manager
	# 	doc=frappe.get_doc("User",manager)

	# 	frappe.throw(f"{manager} =>{doc.name}")
	
	def on_submit(self):
		self.send_notification()


	def send_notification(self):
		message=self.build_message()

		self.send_email(message) 
		self.send_telegram(message)

	
	def send_email(self, message):
		doc=frappe.get_doc("User",self.manager)
		manager_email=doc.email 
		try:
			frappe.sendmail(
				recipients=manager_email,
				subject="Site Progress Report Notification",
				message=message
			)
			frappe.msgprint(f"Message has been sent to  {manager_email}.")
		except Exception as e:
			frappe.throw(f"Failed to send email notification: {e}", title="Email Error")


	def send_telegram(self, message): 
		token=frappe.conf.get("TELEGRAM_BOT_TOKEN")

		chat_id=self.get_password("chat_id")

		if not token or not chat_id:
			frappe.throw(f"Missing telegram credentials.")

		url=f"https://api.telegram.org/bot{token}/sendMessage"

		payload={
			"chat_id":chat_id,
			"text":message,
			"parse_mode":"HTML"
		}

		try:
			requests.post(url,json=payload,timeout=10)
			frappe.msgprint(f"Telegram notification has been sent.")
		except Exception as e:
			frappe.throw(f"Failed to send telegram notification: {e}", title="Telegram Error")


	def build_message(self):
		message = f"Site Progress Report submitted for {self.manager}.\n"
		message += f"Progress Percentage: {self.progress_percentage}%\n"
		message += f"Report Date: {self.report_date}\n"
		return message
	