# Copyright (c) 2026, Mesfin Tsegaye and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests


class MyTodoSettings(Document):
    def on_submit(self):
        self.send_notifications()
        
    def send_notifications(self):
        message = self.build_message()
        self.send_telegram(message)
        
    def send_telegram(self, message):

        token = frappe.conf.get("telegram_bot_token")
        chat_id = self.get_password("chat_id")
        

        if not token or not chat_id:
            frappe.throw("Missing Telegram config", "Telegram Error")
            return

        url = f"https://api.telegram.org/bot{token}/sendMessage"


       

        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            requests.post(url, json=payload, timeout=10)
            
        except Exception as e:
            frappe.throw(str(e), "Telegram Send Failed")
            

    def build_message(self):
        chat_id = self.get_password("chat_id")
        return f"""
				<b>Site Progress Report</b>

				<b>Full Name:</b> {self.full_name}
				<b>Chat ID:</b> {chat_id}
				
				"""

