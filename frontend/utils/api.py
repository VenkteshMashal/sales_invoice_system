import requests

BASE_URL = "http://127.0.0.1:8000"


def get_headers():
    token = None

    try:
        import streamlit as st
        token = st.session_state.get("token")
    except Exception:
        pass

    if token:
        return {"Authorization": f"Bearer {token}"}

    return {}