frappe.ui.form.on("Sales Invoice", {

    refresh(frm) {

        if (!frm.is_new()) {
            frm.add_custom_button(
                "Generate Customers' Invoice Report",
                function () {
                    frappe.call({
                        method:
                        "fshrms.api.invoice_report.generate_invoice_report_background",
                        freeze: true,
                        freeze_message:
                        "Sending report generation to background..."

                    }).then(function(r){
                        frappe.msgprint({
                            title: "Background Job",
                            message: r.message,
                            indicator: "green"
                        });
                    });
                }
            );
        }
    }
});