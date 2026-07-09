frappe.pages["my-todo-page"].on_page_load = function(wrapper) {

    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __("My Page"),
        single_column: true,
    });

    $(page.body).html(`
        <h3>Hello Frappe Page</h3>
    `);

	let field = page.add_field({
    label: 'Status',
    fieldtype: 'Select',
    fieldname: 'status',
    options: [
        'Open',
        'Closed',
        'Cancelled'
    ],
    change() {
        console.log(field.get_value());
    }
});


};


// frappe.pages["my-todo-page"].on_page_load = function(wrapper) {

//     frappe.ui.make_app_page({
//         parent: wrapper,
//         title: __("My Todo Page"),
//         single_column: true,
//     });

//     $(wrapper).find(".page-head").show();

//     $(wrapper).find(".page-title").text("My Todo Page");

//     $(wrapper).find(".layout-main-section").html(`
//         <h3>Hello Frappe Page</h3>
//     `);

	
// };