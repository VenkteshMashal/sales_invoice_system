import streamlit as st
import requests
import pandas as pd
from datetime import date

from utils.api import BASE_URL, get_headers
from utils.auth import require_login, require_company
from utils.layout import render_header

st.set_page_config(page_title="Invoices", page_icon="🧾", layout="wide")

require_login()
require_company()
render_header("🧾 Sales Invoice Management")

company_id = st.session_state["company_id"]

# Load customers
customers_res = requests.get(
    f"{BASE_URL}/customers/company/{company_id}",
    headers=get_headers()
)

# Load products
products_res = requests.get(
    f"{BASE_URL}/products/company/{company_id}",
    headers=get_headers()
)

if customers_res.status_code != 200 or products_res.status_code != 200:
    st.error("Failed to load customers or products.")
    st.stop()

customers = customers_res.json()
products = products_res.json()

if not customers:
    st.warning("Please add customers before creating invoice.")
    st.page_link("pages/4_Customers.py", label="Go to Customers")
    st.stop()

if not products:
    st.warning("Please add products before creating invoice.")
    st.page_link("pages/5_Products.py", label="Go to Products")
    st.stop()

customer_options = {
    f"{c['customer_name']} - {c['phone']}": c["id"]
    for c in customers
}

product_options = {
    f"{p['product_name']} - ₹{p['price_per_unit']} / {p['unit']}": p
    for p in products
}

if "invoice_items" not in st.session_state:
    st.session_state["invoice_items"] = []

st.subheader("Create New Invoice")

selected_customer = st.selectbox(
    "Select Customer",
    list(customer_options.keys())
)

invoice_date = st.date_input("Invoice Date", value=date.today())

st.divider()

st.subheader("Add Products")

col1, col2, col3 = st.columns(3)

with col1:
    selected_product_label = st.selectbox(
        "Select Product",
        list(product_options.keys())
    )

with col2:
    quantity = st.number_input("Quantity", min_value=0.01, step=1.0)

with col3:
    st.write("")
    st.write("")
    add_item = st.button("➕ Add Item")

if add_item:
    product = product_options[selected_product_label]

    amount = float(quantity) * float(product["price_per_unit"])

    st.session_state["invoice_items"].append({
        "product_id": product["id"],
        "item_name": product["product_name"],
        "quantity": quantity,
        "unit": product["unit"],
        "price_per_unit": float(product["price_per_unit"]),
        "amount": amount
    })

    st.success("Item added.")

if st.session_state["invoice_items"]:
    st.subheader("Invoice Items")

    for index, item in enumerate(st.session_state["invoice_items"]):
        col1, col2, col3, col4, col5, col6 = st.columns([3, 1, 1, 1, 1, 1])

        col1.write(item["item_name"])
        col2.write(f"Qty: {item['quantity']}")
        col3.write(item["unit"])
        col4.write(f"₹{item['price_per_unit']}")
        col5.write(f"₹{item['amount']:.2f}")

        if col6.button("❌", key=f"remove_item_{index}"):
            st.session_state["invoice_items"].pop(index)
            st.rerun()

    df_items = pd.DataFrame(st.session_state["invoice_items"])

    sub_total = df_items["amount"].sum()

    gst_amount = st.number_input(
        "GST Amount",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

    total_amount = sub_total + gst_amount

    col1, col2, col3 = st.columns(3)

    col1.metric("Sub Total", f"₹{sub_total:.2f}")
    col2.metric("GST", f"₹{gst_amount:.2f}")
    col3.metric("Total", f"₹{total_amount:.2f}")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("Create Invoice"):
            payload = {
                "customer_id": customer_options[selected_customer],
                "invoice_date": str(invoice_date),
                "gst_amount": gst_amount,
                "items": [
                    {
                        "product_id": item["product_id"],
                        "quantity": item["quantity"]
                    }
                    for item in st.session_state["invoice_items"]
                ]
            }

            response = requests.post(
                f"{BASE_URL}/invoices/company/{company_id}",
                json=payload,
                headers=get_headers()
            )

            if response.status_code == 200:
                created_invoice = response.json()
                st.success(
                    f"Invoice created successfully: {created_invoice['invoice_number']}"
                )
                st.session_state["invoice_items"] = []
                st.rerun()
            else:
                st.error(response.json().get("detail", "Failed to create invoice"))

    with col_b:
        if st.button("Clear Items"):
            st.session_state["invoice_items"] = []
            st.rerun()
            
st.divider()

st.subheader("Invoice History")

invoice_res = requests.get(
    f"{BASE_URL}/invoices/company/{company_id}",
    headers=get_headers()
)

if invoice_res.status_code != 200:
    st.error("Failed to load invoices.")
    st.stop()

invoices = invoice_res.json()

if not invoices:
    st.info("No invoices found.")
    st.stop()

# Customer ID to Name mapping
customer_map = {
    customer["id"]: customer["customer_name"]
    for customer in customers
}

df_invoices = pd.DataFrame(invoices)
df_invoices["customer_name"] = df_invoices["customer_id"].map(customer_map)

display_df = df_invoices[
    [
        "id",
        "invoice_number",
        "customer_name",
        "invoice_date",
        "total_amount",
        "paid_amount",
        "balance_amount",
        "payment_status"
    ]
]

display_df = display_df.rename(columns={
    "id": "ID",
    "invoice_number": "Invoice No",
    "customer_name": "Customer",
    "invoice_date": "Date",
    "total_amount": "Total",
    "paid_amount": "Paid",
    "balance_amount": "Balance",
    "payment_status": "Status"
})

search_invoice = st.text_input("🔍 Search Invoice / Customer")

if search_invoice:
    display_df = display_df[
        display_df["Invoice No"].astype(str).str.contains(search_invoice, case=False, na=False)
        | display_df["Customer"].astype(str).str.contains(search_invoice, case=False, na=False)
    ]

st.dataframe(display_df, width="stretch")

st.divider()

st.subheader("Invoice Actions")

invoice_options = {
    f"{row['invoice_number']} | {row['customer_name']} | ₹{row['total_amount']} | {row['payment_status']}": row
    for _, row in df_invoices.iterrows()
}

selected_invoice_label = st.selectbox(
    "Select Invoice",
    list(invoice_options.keys())
)

selected_invoice = invoice_options[selected_invoice_label]

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👁 View Details"):
        st.write("### Invoice Details")
        st.write(f"**Invoice No:** {selected_invoice['invoice_number']}")
        st.write(f"**Customer:** {selected_invoice['customer_name']}")
        st.write(f"**Date:** {selected_invoice['invoice_date']}")
        st.write(f"**Sub Total:** ₹{selected_invoice['sub_total']}")
        st.write(f"**GST:** ₹{selected_invoice['gst_amount']}")
        st.write(f"**Total:** ₹{selected_invoice['total_amount']}")
        st.write(f"**Paid:** ₹{selected_invoice['paid_amount']}")
        st.write(f"**Balance:** ₹{selected_invoice['balance_amount']}")
        st.write(f"**Status:** {selected_invoice['payment_status']}")
        st.write(f"**Amount in Words:** {selected_invoice['amount_in_words']}")

        st.write("### Items")
        items_df = pd.DataFrame(selected_invoice["items"])
        st.dataframe(items_df, width="stretch")

with col2:
    pdf_response = requests.get(
        f"{BASE_URL}/pdf/invoice/{selected_invoice['id']}/company/{company_id}",
        headers=get_headers()
    )

    if pdf_response.status_code == 200:
        st.download_button(
            label="📄 Download PDF",
            data=pdf_response.content,
            file_name=f"invoice_{selected_invoice['invoice_number'].replace('/', '_')}.pdf",
            mime="application/pdf"
        )
    else:
        st.error("PDF not available.")

with col3:
    if st.button("💰 Go to Payments"):
        st.switch_page("pages/7_Payments.py")