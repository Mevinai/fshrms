// Copyright (c) 2026, Mesfin Tsegaye and contributors
// For license information, please see license.txt

frappe.ui.form.on("My Todo", {

    // refresh(frm) {

    //     frm.add_custom_button(
    //         "Custom Button",
    //         function() {

    //             frappe.msgprint(
    //                 "Thisis a custom button added to existing component."+ frm.doc.title,
    //                 "Custom Button"
    //             );

    //         }
    //     );

    // },

    purchase_invoice(frm) {

        if(frm.doc.purchase_invoice) {
            frm.set_value(
                "description",
                "Purchase Invoice selected automatically: " + frm.doc.purchase_invoice
            );

            frappe.msgprint(
                "Selected Purchase Invoice: "
                + frm.doc.purchase_invoice
            );

        }

    },

    validate(frm) {

        if(!frm.doc.customer_name) {

            frappe.throw(
                "Customer Name is required"
            );

        }

    },

    refresh(frm) {

        frm.add_custom_button(
            "Send Notification",
            function() {


                let dialog = new frappe.ui.Dialog({

                    title: "Send Invoice Notification",

                    fields: [

                        {
                            label: "Message",
                            fieldname: "message",
                            fieldtype: "Small Text",
                            reqd: 1
                        }

                    ],


                    primary_action(values) {

                        frappe.msgprint(
                            "Message Sent: "
                            + values.message
                        );

                        dialog.hide();

                    }

                });
                dialog.show();
            }
        );

    }

});