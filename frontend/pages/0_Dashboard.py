import streamlit as st
import requests

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

    col1.metric("Total Sales", f"₹{float(summary['total_sales']):,.2f}")
    col2.metric("Received", f"₹{float(summary['total_received']):,.2f}")
    col3.metric("Balance", f"₹{float(summary['total_balance']):,.2f}")
    col4.metric("Invoices", summary["total_invoices"])
else:
    st.error("Failed to load summary report.")

st.divider()

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