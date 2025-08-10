// Copyright (c) 2024, earthians Health Informatics Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Patient Billing"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "patient",
            "label": __("Patient"),
            "fieldtype": "Link",
            "options": "Patient",
            "reqd": 1
        },
    ],

    "onload": function(report) {
        // Create a Pie chart after the report is loaded
        let chart_data = {
            labels: ["Help Account", "Paid"],
            datasets: [
                {
                    name: "Status",
                    chartType: "pie",
                    values: [0, 0], // Placeholder values
                }
            ]
        };

        // Create the chart (frappe method to render the chart)
        frappe.chart.create({
            parent: report.page,
            title: "Invoice Status Chart",
            chart_type: "Pie",
            data: chart_data,
            height: 250
        });
    },

    "formatter": function(value, column, data, report) {
        // Highlight status and dynamically update chart
        if (column.fieldname === "status") {
            let chart = report.page.charts[0];  // Access the chart

            // Get current chart data
            let current_data = chart.get_data();

            if (value === "Help Account") {
                // Update Help Account count
                current_data.datasets[0].values[0] += 1;  // Increment Help Account count
                chart.set_data(current_data); // Update chart with new data
                return `<span style="color: red">${value}</span>`;  // Color the status red
            } else if (value === "Paid") {
                // Update Paid count
                current_data.datasets[0].values[1] += 1;  // Increment Paid count
                chart.set_data(current_data); // Update chart with new data
                return `<span style="color: green">${value}</span>`;  // Color the status green
            }
        }
        return value;
    }
};
