import frappe
from frappe import _

def setupTaxAccounts():
	companies = frappe.get_all("Company", pluck="name")
	if not companies:
		return

	for company in companies:
		setupTaxAccountsForCompany(company)


def setupTaxAccountsForCompany(company):
	
	parentAccount = getDutiesTaxesParent(company)
	if not parentAccount:
		frappe.publish_realtime(
			"msgprint",
			_(
				"Could not find parent account '2300 - Duties and Taxes' for company {0}. Please create it manually."
			).format(company),
			raise_comm=False,
		)
		return

	hasNumber = usesAccountNumber(company)

	preferredNumbers = ["2311", "2312", "2313", "2314","2315"]
	usedNumbers = {
		num for num in preferredNumbers if isAccountNumberInUse(company, num)
	}

	availablePool = [num for num in preferredNumbers if num not in usedNumbers]

	taxAccounts = [
		{
			"account_name": "VAT(15%)",
			"account_number": availablePool[0] if len(availablePool) > 0 and hasNumber else None,
			"tax_rate": 15,
		},
		{
			"account_name": "VAT(0)",
			"account_number": availablePool[1] if len(availablePool) > 1 and hasNumber else None,
			"tax_rate": 0,
		},
		{
			"account_name": "VAT(Exempted)",
			"account_number": availablePool[2] if len(availablePool) > 2 and hasNumber else None,
			"tax_rate": 0,
		},
		{
			"account_name": "Excise Tax",
			"account_number": availablePool[3] if len(availablePool) > 3 and hasNumber else None,
			"tax_rate": 0,
		},
		{
			"account_name": "Custom Duty",
			"account_number": availablePool[4] if len(availablePool) > 4 and hasNumber else None,
			"tax_rate": 0,
		},
	]

	for taxAcc in taxAccounts:
		createOrUpdateTaxAccount(
			company,
			parentAccount,
			taxAcc["account_name"],
			taxAcc.get("account_number"),
			taxAcc.get("tax_rate"),
		)

def isAccountNumberInUse(company, accountNumber):
	
	if not accountNumber:
		return False
	return bool(
		frappe.db.get_value(
			"Account",
			{"company": company, "account_number": accountNumber},
			"name",
		)
	)

def usesAccountNumber(company):

	sampleAccount = frappe.get_all(
		"Account",
		filters={
			"company": company,
			"account_number": ["is", "set"],
		},
		fields=["account_number"],
		limit=1,
	)

	return bool(sampleAccount)


def getDutiesTaxesParent(company):

	parentAccount = frappe.db.get_value(
		"Account",
		{
			"company": company,
			"account_number": "2300",
			"account_type": "Tax",
			"root_type": "Liability",
		},
		"name",
	)

	if parentAccount:
		return parentAccount

	parentAccount = frappe.db.get_value(
		"Account",
		{
			"company": company,
			"account_name": "Duties and Taxes",
			"account_type": "Tax",
			"root_type": "Liability",
		},
		"name",
	)

	if parentAccount:
		return parentAccount

	parentAccount = frappe.db.get_value(
		"Account",
		{"company": company, "account_number": "2300"},
		"name",
	)

	if parentAccount:
		accountType = frappe.db.get_value("Account", parentAccount, "account_type")
		rootType = frappe.db.get_value("Account", parentAccount, "root_type")

		if accountType == "Tax" and rootType == "Liability":
			return parentAccount

	parentAccount = frappe.db.get_value(
		"Account",
		{"company": company, "account_name": "Duties and Taxes"},
		"name",
	)

	if parentAccount:
		accountType = frappe.db.get_value("Account", parentAccount, "account_type")
		rootType = frappe.db.get_value("Account", parentAccount, "root_type")

		if accountType == "Tax" and rootType == "Liability":
			return parentAccount

	return None


def createOrUpdateTaxAccount(company, parentAccount, accountName, accountNumber=None, taxRate=None):


	existing = frappe.db.get_value(
		"Account",
		{"company": company, "account_name": accountName},
		"name",
	)

	if existing:
		frappe.db.set_value(
			"Account",
			existing,
			{
				"account_type": "Tax",
				"root_type": "Liability",
				"parent_account": parentAccount,
			},
		)

		if accountNumber:
			frappe.db.set_value(
				"Account",
				existing,
				"account_number",
				accountNumber,
			)

		if taxRate is not None:
			frappe.db.set_value(
				"Account",
				existing,
				"tax_rate",
				taxRate,
			)

		return existing

	accountDoc = frappe.get_doc(
		{
			"doctype": "Account",
			"company": company,
			"account_name": accountName,
			"account_number": accountNumber or "",
			"parent_account": parentAccount,
			"account_type": "Tax",
			"root_type": "Liability",
			"is_group": 0,
			"bank_or_cash": 0,
			"tax_rate": taxRate or 0,
		}
	)

	try:
		accountDoc.insert(ignore_permissions=True)
		frappe.db.commit()

	except Exception as e:
		frappe.db.rollback()
		frappe.publish_realtime(
			"msgprint",
			_("Error creating account {0}: {1}").format(accountName, str(e)),
			raise_comm=False,
		)

	return accountDoc.name if hasattr(accountDoc, "name") and accountDoc.name else None