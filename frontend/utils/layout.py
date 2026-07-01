import streamlit as st
from utils.auth import get_current_owner, logout


def hide_default_sidebar_nav():
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_header(page_title: str):
    hide_default_sidebar_nav()

    owner = get_current_owner()

    st.sidebar.title("🧾 Invoice System")

    st.sidebar.markdown("### 👤 Owner")
    st.sidebar.write(owner["owner_name"])

    st.sidebar.markdown("### 🏢 Active Company")
    st.sidebar.write(st.session_state.get("company_name", "No company selected"))

    st.sidebar.divider()

    st.sidebar.page_link("pages/0_Dashboard.py", label="🏠 Dashboard")
    st.sidebar.page_link("pages/3_Companies.py", label="🏢 Companies")
    st.sidebar.page_link("pages/4_Customers.py", label="👥 Customers")
    st.sidebar.page_link("pages/5_Products.py", label="📦 Products")
    st.sidebar.page_link("pages/6_Invoices.py", label="🧾 Invoices")
    st.sidebar.page_link("pages/7_Payments.py", label="💰 Payments")
    st.sidebar.page_link("pages/8_Reports.py", label="📊 Reports")

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout", width="stretch"):
        logout()

    st.title(page_title)

    if "company_name" in st.session_state:
        st.caption(f"Current Company: {st.session_state['company_name']}")

    st.divider()