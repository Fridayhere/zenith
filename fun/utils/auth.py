import streamlit as st
from supabase import Client
from utils.db import init_connection

def login_user(email, password):
    supabase = init_connection()
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            st.session_state["user"] = res.user
            st.rerun()
    except Exception as e:
        error_message = str(e)
        st.error(f"Login failed: {error_message}")

def signup_user(email, password):
    supabase = init_connection()
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            st.success("Signup successful! You can now log in.")
    except Exception as e:
        error_message = str(e)
        st.error(f"Signup failed: {error_message}")

def check_session():
    if "user" not in st.session_state:
        st.session_state["user"] = None
    return st.session_state["user"]

def logout_user():
    supabase = init_connection()
    try:
        supabase.auth.sign_out()
    except:
        pass
    st.session_state["user"] = None
    st.rerun()
