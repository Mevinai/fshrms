
import frappe

def fdre_salary_calculation(doc,method=None):
    gross= doc.gross_pay

    tax=0 
    if gross <=2000:
        tax=0
    elif gross <=4000:
        tax= (gross * 0.15)-300
    elif gross <=7000:
        tax= (gross * 0.20)-500
    elif gross <=10000:
        tax= (gross * 0.25)-800
    elif gross <=14000:
        tax= (gross * 0.30)-1350
    else:
        tax= (gross * 0.35) - 2050

    tax=max(0,tax)


    doc.append("deductions",{
            "salary_component":"Income tax",
            "amount":tax
        })






