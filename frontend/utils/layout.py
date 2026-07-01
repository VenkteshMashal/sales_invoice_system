import streamlit as st
from utils.auth import get_current_owner, logout


def render_header(page_title: str):
    owner = get_current_owner()

    st.sidebar.title("🧾 Invoice System")
    st.sidebar.success(f"👤 {owner['owner_name']}")

    if "company_name" in st.session_state:
        st.sidebar.info(f"🏢 {st.session_state['company_name']}")

    if st.sidebar.button("Logout"):
        logout()

    st.title(page_title)

    if "company_name" in st.session_state:
        st.caption(f"Current Company: {st.session_state['company_name']}")

    st.divider()