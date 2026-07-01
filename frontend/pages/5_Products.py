import streamlit as st
import requests
import pandas as pd

from utils.api import BASE_URL, get_headers
from utils.auth import require_login, require_company
from utils.layout import render_header

st.set_page_config(page_title="Products", page_icon="📦", layout="wide")

require_login()
require_company()
render_header("📦 Product Management")

company_id = st.session_state["company_id"]

# Add Product
with st.expander("➕ Add New Product"):
    with st.form("add_product_form"):
        col1, col2 = st.columns(2)

        with col1:
            product_name = st.text_input("Product Name")
            unit = st.text_input("Unit", placeholder="Bag / Kg / Piece")

        with col2:
            price_per_unit = st.number_input("Price Per Unit", min_value=0.0, step=1.0)
            description = st.text_area("Description")

        submitted = st.form_submit_button("Save Product")

        if submitted:
            payload = {
                "product_name": product_name,
                "unit": unit,
                "price_per_unit": price_per_unit,
                "description": description
            }

            response = requests.post(
                f"{BASE_URL}/products/company/{company_id}",
                json=payload,
                headers=get_headers()
            )

            if response.status_code == 200:
                st.success("Product added successfully.")
                st.rerun()
            else:
                st.error(response.json().get("detail", "Failed to add product"))

# Load Products
response = requests.get(
    f"{BASE_URL}/products/company/{company_id}",
    headers=get_headers()
)

if response.status_code != 200:
    st.error("Failed to load products.")
    st.stop()

products = response.json()

st.subheader("Product List")

if not products:
    st.info("No products found. Add your first product.")
    st.stop()

df = pd.DataFrame(products)

search = st.text_input("🔍 Search Product")

if search:
    df = df[
        df["product_name"].str.contains(search, case=False, na=False)
        | df["unit"].astype(str).str.contains(search, case=False, na=False)
    ]

st.dataframe(df, width="stretch")

st.divider()

# Delete Product
st.subheader("Delete Product")

product_options = {
    f"{row['product_name']} - ID {row['id']}": row["id"]
    for _, row in df.iterrows()
}

if product_options:
    selected_product = st.selectbox(
        "Select Product to Delete",
        list(product_options.keys())
    )

    confirm_delete = st.checkbox("I confirm I want to delete this product")

    if st.button("Delete Product"):
        if not confirm_delete:
            st.warning("Please confirm before deleting.")
        else:
            product_id = product_options[selected_product]

            delete_response = requests.delete(
                f"{BASE_URL}/products/{product_id}/company/{company_id}",
                headers=get_headers()
            )

            if delete_response.status_code == 200:
                st.success("Product deleted successfully.")
                st.rerun()
            else:
                st.error(delete_response.json().get("detail", "Failed to delete product"))