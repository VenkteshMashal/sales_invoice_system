import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.api import BASE_URL, get_headers
from utils.auth import require_login, require_company
from utils.layout import render_header

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

require_login()
require_company()

render_header("📊 Dashboard")
st.caption("Business overview for selected company")
company_id = st.session_state["company_id"]

# ---------- Summary Cards ----------
summary_response = requests.get(
    f"{BASE_URL}/reports/summary/company/{company_id}",
    headers=get_headers()
)

if summary_response.status_code == 200:
    summary = summary_response.json()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"₹{summary['total_sales']}")
    col2.metric("Received", f"₹{summary['total_received']}")
    col3.metric("Balance", f"₹{summary['total_balance']}")
    col4.metric("Invoices", summary["total_invoices"])
else:
    st.error("Failed to load summary report.")

st.divider()

# ---------- Charts ----------
col1, col2 = st.columns(2)

# with col1:
#     st.subheader("Payment Status")

#     payment_response = requests.get(
#         f"{BASE_URL}/reports/payment-status/company/{company_id}",
#         headers=get_headers()
#     )

#     if payment_response.status_code == 200:
#         payment_data = payment_response.json()

#         if payment_data:
#             df_payment = pd.DataFrame(payment_data)

#             fig, ax = plt.subplots()
#             ax.pie(
#                 df_payment["count"],
#                 labels=df_payment["payment_status"],
#                 autopct="%1.1f%%"
#             )
#             ax.set_title("Payment Status")
#             st.pyplot(fig)
#         else:
#             st.info("No payment data available.")

# with col2:
#     st.subheader("Top Customers")

#     customer_response = requests.get(
#         f"{BASE_URL}/reports/top-customers/company/{company_id}",
#         headers=get_headers()
#     )

#     if customer_response.status_code == 200:
#         customer_data = customer_response.json()

#         if customer_data:
#             df_customers = pd.DataFrame(customer_data)

#             fig, ax = plt.subplots()
#             sns.barplot(
#                 data=df_customers,
#                 x="total_purchase",
#                 y="customer_name",
#                 ax=ax
#             )
#             ax.set_xlabel("Total Purchase")
#             ax.set_ylabel("Customer")
#             st.pyplot(fig)
#         else:
#             st.info("No customer report available.")

# st.divider()

# st.subheader("Product Sales")

# product_response = requests.get(
#     f"{BASE_URL}/reports/product-sales/company/{company_id}",
#     headers=get_headers()
# )

# if product_response.status_code == 200:
#     product_data = product_response.json()

#     if product_data:
#         df_products = pd.DataFrame(product_data)

#         fig, ax = plt.subplots()
#         sns.barplot(
#             data=df_products,
#             x="item_name",
#             y="total_amount",
#             ax=ax
#         )
#         ax.set_xlabel("Product")
#         ax.set_ylabel("Total Sales Amount")
#         st.pyplot(fig)

#         st.dataframe(df_products, width="stretch")
#     else:
#         st.info("No product sales data available.")
    
# st.divider()

st.subheader("Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.page_link("pages/4_Customers.py", label="👥 Customers")

with col2:
    st.page_link("pages/5_Products.py", label="📦 Products")

with col3:
    st.page_link("pages/6_Invoices.py", label="🧾 Invoices")

with col4:
    st.page_link("pages/7_Payments.py", label="💰 Payments")