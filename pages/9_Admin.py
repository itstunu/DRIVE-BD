import streamlit as st
import auth
import pandas as pd
from db import get_user_by_email, create_user_in_db, get_users, get_vehicles, get_violations, get_payments

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="Admin - DriveBD",
    page_icon="👑",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()
auth.require_role('admin')

# ---- Page Content ----
st.title("👑 Admin Panel")

# ---- Dashboard Stats ----
col1, col2, col3, col4 = st.columns(4)

# Get data (you'll need to add get_users function)
# For now using sample counts
vehicles = get_vehicles()
violations = get_violations()
payments = get_payments()

with col1:
    st.metric("👤 Total Users", "0")
with col2:
    st.metric("🚗 Total Vehicles", len(vehicles))
with col3:
    st.metric("⚠️ Total Violations", len(violations))
with col4:
    total_paid = sum([p.get('amount', 0) for p in payments if p.get('status') == 'completed'])
    st.metric("💰 Total Revenue", f"${total_paid:,.2f}")

st.divider()

# ---- Admin Actions ----
tab1, tab2, tab3 = st.tabs(["👤 Manage Users", "⚙️ System Settings", "📊 System Logs"])

with tab1:
    st.info("User management coming soon!")
    # Add user management here

with tab2:
    st.info("System settings coming soon!")
    # Add settings here

with tab3:
    st.info("System logs coming soon!")
    # Add logs here