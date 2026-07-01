import streamlit as st

st.set_page_config(
    page_title="Sales Invoice System",
    page_icon="🧾",
    layout="centered"
)

st.title("🧾 Sales Invoice Management System")
st.write("Create invoices, track payments, generate PDFs, and view business reports.")

if "token" in st.session_state:
    st.success("You are already logged in.")
    st.page_link("pages/0_Dashboard.py", label="Go to Dashboard", icon="📊")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.page_link("pages/2_Login.py", label="Login", icon="🔐")

    with col2:
        st.page_link("pages/1_Register.py", label="Register", icon="📝")