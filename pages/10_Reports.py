import streamlit as st
import auth
import pandas as pd
from db import get_vehicles, get_violations, get_payments
from datetime import datetime, timedelta

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="Reports - DriveBD",
    page_icon="📈",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()

# ---- Page Content ----
st.title("📈 Reports")

# ---- Date Filter ----
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
with col2:
    end_date = st.date_input("End Date", datetime.now())

# ---- Get Data ----
vehicles = get_vehicles()
violations = get_violations()
payments = get_payments()

# ---- Report Tabs ----
tab1, tab2, tab3 = st.tabs(["🚗 Vehicle Report", "⚠️ Violation Report", "💰 Payment Report"])

with tab1:
    st.subheader("Vehicle Registration Report")
    st.metric("Total Vehicles", len(vehicles))
    # Add more vehicle metrics here

with tab2:
    st.subheader("Violation Report")
    st.metric("Total Violations", len(violations))
    # Add violation metrics here

with tab3:
    st.subheader("Payment Report")
    total = sum([p.get('amount', 0) for p in payments if p.get('status') == 'completed'])
    st.metric("Total Payments", f"${total:,.2f}")
    # Add payment metrics here