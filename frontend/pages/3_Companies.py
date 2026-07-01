import streamlit as st
import requests
import pandas as pd

from utils.api import BASE_URL, get_headers

st.set_page_config(page_title="Companies", page_icon="🏢", layout="wide")

st.title("🏢 Company Management")

if "token" not in st.session_state:
    st.warning("Please login first.")
    st.page_link("pages/2_Login.py", label="Go to Login")
    st.stop()

st.subheader("Add Company")

with st.form("add_company_form"):
    company_name = st.text_input("Company Name")
    address = st.text_area("Address")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    state = st.text_input("State")

    submitted = st.form_submit_button("Add Company")

    if submitted:
        payload = {
            "company_name": company_name,
            "address": address,
            "phone": phone,
            "email": email if email else None,
            "state": state
        }

        response = requests.post(
            f"{BASE_URL}/companies/",
            json=payload,
            headers=get_headers()
        )

        if response.status_code == 200:
            st.success("Company added successfully.")
            st.rerun()
        else:
            st.error(response.json().get("detail", "Failed to add company"))

st.divider()

st.subheader("Your Companies")

response = requests.get(
    f"{BASE_URL}/companies/",
    headers=get_headers()
)

if response.status_code == 200:
    companies = response.json()

    if companies:
        df = pd.DataFrame(companies)
        st.dataframe(df, use_container_width=True)

        company_options = {
            f"{company['company_name']} - ID {company['id']}": company
            for company in companies
        }

        selected = st.selectbox(
            "Select Active Company",
            list(company_options.keys())
        )

        if st.button("Use This Company"):
            selected_company = company_options[selected]

            st.session_state["company_id"] = selected_company["id"]
            st.session_state["company_name"] = selected_company["company_name"]

            st.success(f"Active company selected: {selected_company['company_name']}")
            st.switch_page("pages/0_Dashboard.py")
    else:
        st.info("No companies found. Add your first company.")
else:
    st.error("Failed to load companies.")