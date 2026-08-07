"""
DriveBD - Authentication & Role-Based Access Control
Simple bcrypt-based auth using Streamlit session_state (no external auth service needed).
"""
import bcrypt
import streamlit as st
from db import get_user_by_email, create_user_in_db, log_activity_db

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def log_activity(user_id, action, details=None):
    """Log user activity"""
    try:
        log_activity_db(user_id, action, details)
    except Exception:
        pass  # Silently fail if logging doesn't work


def login(email: str, password: str) -> bool:
    """Login user using Supabase"""
    try:
        user = get_user_by_email(email.strip().lower())
        
        if user and verify_password(password, user.get('password_hash', '')):
            st.session_state["auth"] = {
                "user_id": user.get('id'),
                "name": user.get('name'),
                "email": user.get('email'),
                "role": user.get('role'),
                "nid": user.get('nid'),
                "phone": user.get('phone'),
                "license_no": user.get('license_no'),
            }
            log_activity(user.get('id'), "Logged in")
            return True
        return False
    except Exception as e:
        print(f"Login error: {e}")
        return False


def logout():
    if "auth" in st.session_state:
        log_activity(st.session_state["auth"]["user_id"], "Logged out")
    st.session_state.pop("auth", None)


def is_logged_in() -> bool:
    return "auth" in st.session_state


def current_user():
    return st.session_state.get("auth")


def require_login():
    """Call at the top of every protected page. Stops rendering if not logged in."""
    if not is_logged_in():
        st.warning("Please log in from the Home page to access this section.")
        st.stop()


def require_role(*allowed_roles):
    """Call at the top of a page to restrict it to specific roles."""
    require_login()
    role = current_user()["role"]
    if role not in allowed_roles:
        st.error(f"Access denied. This page is restricted to: {', '.join(allowed_roles)}.")
        st.stop()


def register_user(name, email, password, role, nid="", phone="", license_no=""):
    """Register a new user using Supabase"""
    try:
        # Check if user already exists
        existing = get_user_by_email(email.strip().lower())
        if existing:
            return False, "An account with this email already exists."
        
        user_data = {
            "name": name,
            "email": email.strip().lower(),
            "password_hash": hash_password(password),
            "role": role,
            "nid": nid,
            "phone": phone,
            "license_no": license_no,
        }
        
        new_user = create_user_in_db(user_data)
        if new_user:
            return True, "Account created successfully. Please log in."
        else:
            return False, "Account creation failed. Please try again."
    except Exception as e:
        return False, f"Error creating account: {str(e)}"
