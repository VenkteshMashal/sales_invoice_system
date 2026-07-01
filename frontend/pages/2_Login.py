import streamlit as st
import requests
from utils.api import BASE_URL

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

st.title("🔐 Owner Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=payload)

    if response.status_code == 200:
        data = response.json()
        st.session_state["token"] = data["access_token"]
        st.success("Login successful.")
        st.switch_page("pages/3_Companies.py")
    else:
        st.error(response.json().get("detail", "Login failed")) 