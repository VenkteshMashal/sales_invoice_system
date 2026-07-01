import streamlit as st
import requests
from utils.api import BASE_URL

st.set_page_config(page_title="Register", page_icon="📝", layout="centered")

st.title("📝 Owner Register")

owner_name = st.text_input("Owner Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):
    payload = {
        "owner_name": owner_name,
        "email": email,
        "password": password
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=payload)

    if response.status_code == 200:
        st.success("Registration successful. Please login.")
        st.page_link("pages/2_Login.py", label="Go to Login", icon="🔐")
    else:
        st.error(response.json().get("detail", "Registration failed"))