import streamlit as st
import auth
from db import get_vehicles, get_violations, get_payments, get_notifications
import pandas as pd
from datetime import datetime

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="Dashboard - DriveBD",
    page_icon="📊",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()

# ---- Page Content ----
st.title("📊 Dashboard")
st.write(f"Welcome back, **{auth.current_user()['name']}**!")

# Get current user
user = auth.current_user()
user_id = user.get('user_id')

# ---- Metrics ----
col1, col2, col3, col4 = st.columns(4)

# Get data
vehicles = get_vehicles(user_id)
violations = get_violations()
payments = get_payments(user_id)
notifications = get_notifications(user_id)

with col1:
    st.metric("🚗 Vehicles", len(vehicles))
with col2:
    pending_violations = [v for v in violations if v.get('status') == 'pending']
    st.metric("⚠️ Pending Violations", len(pending_violations))
with col3:
    unread = [n for n in notifications if not n.get('is_read', False)]
    st.metric("🔔 Unread Notifications", len(unread))
with col4:
    total_paid = sum([p.get('amount', 0) for p in payments if p.get('status') == 'completed'])
    st.metric("💰 Total Paid", f"${total_paid:,.2f}")

st.divider()

# ---- Recent Activity ----
st.subheader("📋 Recent Activity")

if notifications:
    recent = notifications[:5]
    for n in recent:
        st.info(f"🔔 **{n.get('title', 'Notification')}** - {n.get('message', '')}")
else:
    st.info("No recent activity")

st.divider()

# ---- Quick Actions ----
st.subheader("⚡ Quick Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚗 Add Vehicle", use_container_width=True):
        st.switch_page("pages/2_Vehicles.py")

with col2:
    if st.button("💰 Make Payment", use_container_width=True):
        st.switch_page("pages/4_Payments.py")

with col3:
    if st.button("📄 Upload Document", use_container_width=True):
        st.switch_page("pages/5_Documents.py")