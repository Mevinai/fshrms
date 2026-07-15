#fshrms/api/invoice_report.py

import frappe
from io import BytesIO
from openpyxl import Workbook
from frappe.utils import now_datetime

@frappe.whitelist()
def generate_invoice_report_background():

    user = frappe.session.user

    frappe.enqueue(
        "fshrms.api.invoice_report.create_customer_invoice_report",
        queue="long",
        timeout=1500,
        user=user
    )

    return "Report generation started in background"


def create_customer_invoice_report(user):

    customers = frappe.get_all(
        "Customer",
        fields=["name", "customer_name"]
    )

    wb = Workbook()

    ws = wb.active
    ws.title = "Customer Invoice Summary"

    ws.append([
        "Customer",
        "Invoice Count",
        "Total Sales",
        "Outstanding"
    ])

    detail = wb.create_sheet(
        "Invoice Details"
    )

    detail.append([
        "Customer",
        "Invoice",
        "Date",
        "Amount",
        "Outstanding",
        "Status"
    ])

    for customer in customers:

        invoices = frappe.get_all(
            "Sales Invoice",
            filters={
                "customer": customer.name,
                # "docstatus": 1 # Draft=0, Submitted=1, Cancelled=2
            },
            fields=[
                "name",
                "posting_date",
                "grand_total",
                "outstanding_amount",
                "status"
            ]
        )

        if not invoices:
            continue

        total = 0
        outstanding = 0

        for inv in invoices:

            total += inv.grand_total
            outstanding += inv.outstanding_amount

            detail.append([
                customer.customer_name,
                inv.name,
                inv.posting_date,
                inv.grand_total,
                inv.outstanding_amount,
                inv.status
            ])

        ws.append([
            customer.customer_name,
            len(invoices),
            total,
            outstanding
        ])

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    file = frappe.get_doc({
        "doctype": "File",
        "file_name":
        f"Customer Invoice Report {now_datetime()}.xlsx",
        "content": output.read(),
        "is_private": 1
    })

    file.insert()

    send_report_email(file)

    frappe.publish_realtime(
        event="msgprint",
        message="Customer Invoice Report generated successfully and has been sent via email in realtime mode.",
        user=user
    )

def send_report_email(file):

    recipients = [
        "sciemesfin55@gmail.com",
        "mesfin.tmaniye@gmail.com"
    ]

    frappe.sendmail(

        recipients=recipients,

        subject=
        "Customer Sales Invoice Report",

        message="""
        Hello,

        The customer sales invoice report
        has been generated.

        Please find the attachment.

        Regards
        ERPNext
        """,

        attachments=[
            {
                "fname": file.file_name,
                "fcontent": file.get_content()
            }
        ]

    )


def scheduled_customer_invoice_report():
    user = frappe.session.user
    frappe.enqueue(
        "fshrms.api.invoice_report.create_customer_invoice_report",
        queue="long",
        timeout=1500,
        user=user
    )