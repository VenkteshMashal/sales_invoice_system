import streamlit as st
import requests
from utils.api import BASE_URL, get_headers


def require_login():
    if "token" not in st.session_state:
        st.warning("Please login first.")
        st.page_link("pages/2_Login.py", label="Go to Login", icon="🔐")
        st.stop()


def get_current_owner():
    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers=get_headers()
    )

    if response.status_code == 200:
        return response.json()

    st.session_state.clear()
    st.warning("Session expired. Please login again.")
    st.page_link("pages/2_Login.py", label="Go to Login", icon="🔐")
    st.stop()


def require_company():
    if "company_id" not in st.session_state:
        st.warning("Please select a company first.")
        st.page_link("pages/3_Companies.py", label="Select Company", icon="🏢")
        st.stop()


def logout():
    st.session_state.clear()
    st.success("Logged out successfully.")
    st.switch_page("Home.py")