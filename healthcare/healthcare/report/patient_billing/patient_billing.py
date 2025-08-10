import frappe

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Invoice ID", "fieldname": "invoice_id", "fieldtype": "Link", "options": "Sales Invoice", "width": 200},
        {"label": "Invoice Date", "fieldname": "invoice_date", "fieldtype": "Date", "width": 100},
        {"label": "Patient", "fieldname": "patient", "fieldtype": "Link", "options": "Patient", "width": 150},
        {"label": "Service", "fieldname": "service", "fieldtype": "Data", "width": 300},
        {"label": "Total Amount", "fieldname": "total", "fieldtype": "Currency", "width": 100},
        {"label": "Paid Amount", "fieldname": "net_total", "fieldtype": "Currency", "width": 100},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]

def get_data(filters):
    conditions = []
    if filters.get("from_date") and filters.get("to_date"):
        conditions.append("si.posting_date BETWEEN %(from_date)s AND %(to_date)s")
    if filters.get("customer"):
        conditions.append("si.customer = %(customer)s")
    if filters.get("patient"):
        conditions.append("si.patient = %(patient)s")

    # Join all conditions with AND; if no conditions, defaults to "1=1"
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT
            si.name AS invoice_id,
            si.posting_date AS invoice_date,
            si.customer,
            si.patient,
            GROUP_CONCAT(sii.item_name SEPARATOR ', ') AS service,
            si.total AS total,
            si.net_total AS net_total
        FROM
            `tabSales Invoice` si
        LEFT JOIN
            `tabSales Invoice Item` sii ON sii.parent = si.name
        WHERE
            {where_clause}
        GROUP BY
            si.name
        ORDER BY
            si.posting_date DESC
    """
    data = frappe.db.sql(query, filters, as_dict=True)

    # Update status based on the total amount
    for row in data:
        if row["net_total"] <= 1:
            row["status"] = "Help Account"
        else:
            row["status"] = "Paid"

    return data
