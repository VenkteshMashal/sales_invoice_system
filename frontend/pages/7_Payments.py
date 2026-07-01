import streamlit as st
import requests
import pandas as pd

from utils.api import BASE_URL, get_headers
from utils.auth import require_login, require_company
from utils.layout import render_header

st.set_page_config(page_title="Payments", page_icon="💰", layout="wide")

require_login()
require_company()
render_header("💰 Payment Management")

company_id = st.session_state["company_id"]

# Load invoices
invoice_res = requests.get(
    f"{BASE_URL}/invoices/company/{company_id}",
    headers=get_headers()
)

if invoice_res.status_code != 200:
    st.error("Failed to load invoices.")
    st.stop()

invoices = invoice_res.json()

if not invoices:
    st.info("No invoices found. Create an invoice first.")
    st.page_link("pages/6_Invoices.py", label="Go to Invoices", icon="🧾")
    st.stop()

df = pd.DataFrame(invoices)

st.subheader("Invoice Payment Status")

display_df = df[
    [
        "id",
        "invoice_number",
        "customer_id",
        "invoice_date",
        "total_amount",
        "paid_amount",
        "balance_amount",
        "payment_status",
    ]
]

search = st.text_input("🔍 Search Invoice Number")

if search:
    display_df = display_df[
        display_df["invoice_number"].astype(str).str.contains(search, case=False, na=False)
    ]

st.dataframe(display_df, width="stretch")

st.divider()

st.subheader("Update Payment")

invoice_options = {
    f"{row['invoice_number']} | Total ₹{row['total_amount']} | Balance ₹{row['balance_amount']}": row
    for _, row in df.iterrows()
}

selected_invoice_label = st.selectbox(
    "Select Invoice",
    list(invoice_options.keys())
)

selected_invoice = invoice_options[selected_invoice_label]

col1, col2, col3 = st.columns(3)

col1.metric("Total Amount", f"₹{selected_invoice['total_amount']}")
col2.metric("Already Paid", f"₹{selected_invoice['paid_amount']}")
col3.metric("Balance", f"₹{selected_invoice['balance_amount']}")

st.write(f"Current Status: **{selected_invoice['payment_status']}**")

new_paid_amount = st.number_input(
    "Enter Total Paid Amount Till Now",
    min_value=0.0,
    value=float(selected_invoice["paid_amount"]),
    step=1.0
)

if st.button("Update Payment"):
    payload = {
        "paid_amount": new_paid_amount
    }

    response = requests.put(
        f"{BASE_URL}/payments/invoice/{selected_invoice['id']}/company/{company_id}",
        json=payload,
        headers=get_headers()
    )

    if response.status_code == 200:
        updated_invoice = response.json()
        st.success(
            f"Payment updated. Status: {updated_invoice['payment_status']}, "
            f"Balance: ₹{updated_invoice['balance_amount']}"
        )
        st.rerun()
    else:
        st.error(response.json().get("detail", "Failed to update payment"))