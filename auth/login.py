import streamlit as st
import re
from auth.db import hash_password, verify_user, create_user, create_table

# Ensure the table exists
create_table()

# Session Management
def is_user_authenticated():
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        return True
    return False

def show_login_page():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        hashed_password = hash_password(password)
        if verify_user(username.lower(), hashed_password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid username or password")
    if st.button("Go to Sign Up", key="go_to_signup"):
        st.session_state.show_login = False
        st.rerun()

def show_signup_page():
    st.title("Sign Up")
    username = st.text_input("Username", key="signup_username")
    name = st.text_input("Name", key="signup_name")
    password = st.text_input("Password", type="password", key="signup_password")
    st.caption("Password must contain a mix of alphabets, numbers, and special characters.")
    if st.button("Sign Up", key="signup_button"):
        # Validate username and password
        if not username.islower():
            st.error("Username must be in small letters.")
            return
        if not re.search(r"[a-zA-Z]", password) or not re.search(r"\d", password) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            st.error("Password must contain a mix of alphabets, numbers, and special characters.")
            return

        hashed_password = hash_password(password)
        if create_user(username.lower(), name, hashed_password):
            st.success("User created successfully. Please log in.")
            st.session_state.show_login = True
            st.rerun()
        else:
            st.error("Username already exists. Please choose a different username.")
    if st.button("Go to Login", key="go_to_login"):
        st.session_state.show_login = True
        st.rerun()