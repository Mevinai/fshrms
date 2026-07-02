import frappe


def calculate_fdre_income_tax(doc, method):
    gross_pay = doc.gross_pay or 0

    tax = get_fdre_income_tax(gross_pay)

    # Replace Income Tax deduction
    for row in doc.deductions:
        if row.salary_component == "Income Tax":
            row.amount = tax
            break

    # Recalculate totals
    doc.total_deduction = sum(d.amount for d in doc.deductions)
    doc.net_pay = doc.gross_pay - doc.total_deduction
    doc.rounded_total = doc.net_pay


def get_fdre_income_tax(gross_pay):
    if gross_pay <= 2000:
        return 0
    elif gross_pay <= 4000:
        return gross_pay * 0.15 - 300
    elif gross_pay <= 7000:
        return gross_pay * 0.20 - 500
    elif gross_pay <= 10000:
        return gross_pay * 0.25 - 850
    elif gross_pay <= 14000:
        return gross_pay * 0.30 - 1350
    else:
        return gross_pay * 0.35 - 2050