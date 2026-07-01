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

    df_items = pd.DataFrame(st.session_state["invoice_items"])
    st.dataframe(df_items, width="stretch")

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

if invoice_res.status_code == 200:
    invoices = invoice_res.json()

    if invoices:
        df_invoices = pd.DataFrame(invoices)
        st.dataframe(df_invoices, width="stretch")
    else:
        st.info("No invoices found.")
else:
    st.error("Failed to load invoices.")