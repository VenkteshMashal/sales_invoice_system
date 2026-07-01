import streamlit as st
import requests
import pandas as pd

from utils.api import BASE_URL, get_headers
from utils.auth import require_login, require_company
from utils.layout import render_header

st.set_page_config(page_title="Customers", page_icon="👥", layout="wide")

require_login()
require_company()
render_header("👥 Customer Management")

company_id = st.session_state["company_id"]

# ---------- Add Customer ----------
with st.expander("➕ Add New Customer"):
    with st.form("add_customer_form"):
        col1, col2 = st.columns(2)

        with col1:
            customer_name = st.text_input("Customer Name")
            phone = st.text_input("Phone Number")
            email = st.text_input("Email")
            gst_number = st.text_input("GST Number")

        with col2:
            city = st.text_input("City")
            state = st.text_input("State")
            pin_code = st.text_input("PIN Code")
            address = st.text_area("Address")

        submitted = st.form_submit_button("Save Customer")

        if submitted:
            payload = {
                "customer_name": customer_name,
                "phone": phone,
                "email": email if email else None,
                "address": address,
                "city": city,
                "state": state,
                "pin_code": pin_code,
                "gst_number": gst_number
            }

            response = requests.post(
                f"{BASE_URL}/customers/company/{company_id}",
                json=payload,
                headers=get_headers()
            )

            if response.status_code == 200:
                st.success("Customer added successfully.")
                st.rerun()
            else:
                st.error(response.json().get("detail", "Failed to add customer"))

# ---------- Load Customers ----------
response = requests.get(
    f"{BASE_URL}/customers/company/{company_id}",
    headers=get_headers()
)

if response.status_code != 200:
    st.error("Failed to load customers.")
    st.stop()

customers = response.json()

st.subheader("Customer List")

if not customers:
    st.info("No customers found.")
    st.stop()

df = pd.DataFrame(customers)

search = st.text_input("🔍 Search Customer")

if search:
    df = df[
        df["customer_name"].str.contains(search, case=False, na=False)
        | df["phone"].astype(str).str.contains(search, case=False, na=False)
        | df["city"].astype(str).str.contains(search, case=False, na=False)
    ]

st.dataframe(df, width="stretch")

st.divider()

# ---------- Delete Customer ----------
st.subheader("Delete Customer")

customer_options = {
    f"{row['customer_name']} - ID {row['id']}": row["id"]
    for _, row in df.iterrows()
}

if customer_options:
    selected_customer = st.selectbox(
        "Select Customer to Delete",
        list(customer_options.keys())
    )

    if st.button("Delete Customer"):
        customer_id = customer_options[selected_customer]

        delete_response = requests.delete(
            f"{BASE_URL}/customers/{customer_id}/company/{company_id}",
            headers=get_headers()
        )

        if delete_response.status_code == 200:
            st.success("Customer deleted successfully.")
            st.rerun()
        else:
            st.error(delete_response.json().get("detail", "Failed to delete customer"))