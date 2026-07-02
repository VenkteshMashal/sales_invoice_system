import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.api import BASE_URL, get_headers
from utils.auth import require_login, require_company
from utils.layout import render_header

def format_currency(amount):
    return f"₹{float(amount):,.2f}"

st.set_page_config(page_title="Reports", page_icon="📊", layout="wide")

require_login()
require_company()
render_header("📊 Reports")

company_id = st.session_state["company_id"]

# Summary
summary_res = requests.get(
    f"{BASE_URL}/reports/summary/company/{company_id}",
    headers=get_headers()
)

if summary_res.status_code == 200:
    summary = summary_res.json()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", format_currency(summary["total_sales"]))
    col2.metric("Received", format_currency(summary["total_received"]))
    col3.metric("Balance", format_currency(summary["total_balance"]))
    col4.metric("Invoices", summary["total_invoices"])

st.divider()

# Payment Status
st.subheader("Payment Status")

payment_res = requests.get(
    f"{BASE_URL}/reports/payment-status/company/{company_id}",
    headers=get_headers()
)

if payment_res.status_code == 200:
    payment_data = payment_res.json()

    if payment_data:
        df_payment = pd.DataFrame(payment_data)

        fig, ax = plt.subplots()
        ax.pie(
            df_payment["count"],
            labels=df_payment["payment_status"],
            autopct="%1.1f%%"
        )
        st.pyplot(fig)
        st.dataframe(df_payment, width="stretch")
    else:
        st.info("No payment data available.")

st.divider()

# Top Customers
st.subheader("Top Customers")

customer_res = requests.get(
    f"{BASE_URL}/reports/top-customers/company/{company_id}",
    headers=get_headers()
)

if customer_res.status_code == 200:
    customer_data = customer_res.json()

    if customer_data:
        df_customers = pd.DataFrame(customer_data)
        df_customers_chart = df_customers.copy()
        df_customers["total_purchase"] = df_customers["total_purchase"].apply(format_currency)

        fig, ax = plt.subplots()
        sns.barplot(
            data=df_customers,
            x="total_purchase",
            y="customer_name",
            ax=ax
        )
        st.pyplot(fig)
        st.dataframe(df_customers, width="stretch")
    else:
        st.info("No customer report available.")

st.divider()

# Product Sales
st.subheader("Product Sales")

product_res = requests.get(
    f"{BASE_URL}/reports/product-sales/company/{company_id}",
    headers=get_headers()
)

if product_res.status_code == 200:
    product_data = product_res.json()

    if product_data:
        df_products = pd.DataFrame(product_data)
        df_products_chart = df_products.copy()
        df_products["total_amount"] = df_products["total_amount"].apply(format_currency)

        fig, ax = plt.subplots()
        sns.barplot(
            data=df_products,
            x="item_name",
            y="total_amount",
            ax=ax
        )
        st.pyplot(fig)
        st.dataframe(df_products, width="stretch")
    else:
        st.info("No product sales data available.")