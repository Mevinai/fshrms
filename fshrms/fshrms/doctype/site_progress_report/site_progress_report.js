// Copyright (c) 2026, Mesfin Tsegaye and contributors
// For license information, please see license.txt

frappe.ui.form.on("Site Progress Report", {
    // refresh(frm) {
    //     frm.add_custom_button(
    //         "Custom Button",
    //         function() {
    //             frappe.msgprint(
    //                 "Hey. This is a project: "+ frm.doc.project+" => "+ frm.doc.workers_on_site+ " , Manager: "+frm.doc.manager
    //             );
    //         }
    //     );
    // //  Get attribute
    // //   console.log(frm.doc.project);
    // },

    manager(frm) {
        if (frm.doc.manager) {
            frappe.msgprint(
                "Selected Customer: "
                + frm.doc.manager
            );
        }
    },

    refresh(frm) {
        frm.add_custom_button(
            "Send Notification",
            function () {
                let dialog = new frappe.ui.Dialog({
                    title: "Send Invoice Notification",
                    fields: [
                        {
                            label: 'First Name',
                            fieldname: 'first_name',
                            fieldtype: 'Data'
                        },
                        {
                            label: 'Last Name',
                            fieldname: 'last_name',
                            fieldtype: 'Data'
                        },
                        {
                            label: 'Age',
                            fieldname: 'age',
                            fieldtype: 'Int'
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
