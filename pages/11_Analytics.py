import streamlit as st
import auth
import pandas as pd
import plotly.express as px
from db import get_vehicles, get_violations, get_payments

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="Analytics - DriveBD",
    page_icon="📉",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()

# ---- Page Content ----
st.title("📉 Analytics Dashboard")

# ---- Get Data ----
vehicles = get_vehicles()
violations = get_violations()
payments = get_payments()

# ---- Charts ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚗 Vehicles by Status")
    if vehicles:
        df_vehicles = pd.DataFrame(vehicles)
        status_counts = df_vehicles['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig = px.pie(status_counts, values='Count', names='Status', title="Vehicle Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No vehicle data available")

with col2:
    st.subheader("⚠️ Violations by Type")
    if violations:
        df_violations = pd.DataFrame(violations)
        type_counts = df_violations['violation_type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        fig = px.bar(type_counts, x='Type', y='Count', title="Violation Types")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No violation data available")

st.divider()

st.subheader("💰 Payment Analytics")
if payments:
    df_payments = pd.DataFrame(payments)
    total_paid = df_payments[df_payments['status'] == 'completed']['amount'].sum()
    st.metric("Total Revenue", f"${total_paid:,.2f}")
else:
    st.info("No payment data available")