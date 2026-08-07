"""
DriveBD - Authentication & Role-Based Access Control
Using Supabase for user management
"""
import bcrypt
import streamlit as st
from db import get_user_by_email, create_user
from datetime import datetime

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

def login(email: str, password: str) -> bool:
    """Authenticate user and set session state"""
    try:
        user = get_user_by_email(email)
        if user and verify_password(password, user['password_hash']):
            st.session_state["auth"] = {
                "user_id": user['id'],
                "name": user['name'],
                "email": user['email'],
                "role": user['role'],
            }
            # Log activity (optional)
            try:
                log_activity(user['id'], "Logged in")
            except:
                pass
            return True
        return False
    except Exception as e:
        print(f"Login error: {e}")
        return False

def logout():
    """Clear session state and logout"""
    if "auth" in st.session_state:
        try:
            log_activity(st.session_state["auth"]["user_id"], "Logged out")
        except:
            pass
        st.session_state.pop("auth", None)

def is_logged_in() -> bool:
    """Check if user is logged in"""
    return "auth" in st.session_state

def current_user():
    """Get current user info"""
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
    """Register a new user"""
    try:
        # Check if user already exists
        existing = get_user_by_email(email)
        if existing:
            return False, "An account with this email already exists."
        
        # Create new user
        user_data = {
            "name": name,
            "email": email.lower().strip(),
            "password_hash": hash_password(password),
            "role": role,
            "nid": nid,
            "phone": phone,
            "license_no": license_no,
            "created_at": datetime.now().isoformat()
        }
        
        user = create_user(user_data)
        if user:
            return True, "Account created successfully. Please log in."
        else:
            return False, "Error creating account. Please try again."
    except Exception as e:
        print(f"Registration error: {e}")
        return False, f"Error creating account: {str(e)}"

def log_activity(user_id, action):
    """Log user activity (requires activity_logs table)"""
    try:
        from db import supabase
        from datetime import datetime
        
        activity_data = {
            "user_id": user_id,
            "action": action,
            "timestamp": datetime.now().isoformat()
        }
        supabase.table('activity_logs').insert(activity_data).execute()
    except Exception as e:
        print(f"Error logging activity: {e}")
