import streamlit as st
import auth
import pandas as pd
from datetime import datetime

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="Service History - DriveBD",
    page_icon="🔧",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()

# ---- Page Content ----
st.title("🔧 Service History")
st.info("This feature will be available in the next update. Track your vehicle service records here.")

# Sample data display (to be connected to database)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔧 Total Services", "0")
with col2:
    st.metric("📅 Last Service", "N/A")
with col3:
    st.metric("💰 Total Spent", "$0.00")

st.divider()

# Placeholder for service records
st.warning("Service history tracking coming soon! You'll be able to:")
st.markdown("""
- ✅ Log service visits
- ✅ Track maintenance costs
- ✅ Set service reminders
- ✅ View service history by vehicle
""")