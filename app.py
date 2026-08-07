import streamlit as st
import pandas as pd
from db import get_vehicles, get_violations, get_payments, get_notifications
import auth

# ---- Page Config ----
st.set_page_config(page_title="Dashboard - DriveBD", page_icon="📊", layout="wide")

# ---- Auth Check ----
auth.require_login()
user = auth.current_user()

st.title("📊 Dashboard")
st.caption(f"Welcome back, {user['name']}")

# ---- Get Data ----
if user["role"].lower() == "admin":
    vehicles = get_vehicles()
    violations = get_violations()
    payments = get_payments()
else:
    vehicles = get_vehicles(user["user_id"])
    violation_list = []
    for v in vehicles:
        violation_list.extend(get_violations(v.get("registration_number")))
    violations = violation_list
    payments = get_payments(user["user_id"])

# ---- Calculate Stats ----
unpaid_fines = sum(v.get("fine_amount", 0) for v in violations if v.get("status") == "unpaid")
unread_count = len([n for n in get_notifications(user["user_id"]) if not n.get("is_read", False)])

# ---- Display Metrics ----
c1, c2, c3, c4 = st.columns(4)
c1.metric("Vehicles" if user["role"] != "admin" else "Total Vehicles", len(vehicles))
c2.metric("Violations", len(violations))
c3.metric("Unpaid Fines (BDT)", f"{unpaid_fines:,.0f}")
c4.metric("Unread Notifications", unread_count)

st.divider()

# ---- Recent Violations ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("Recent Violations")
    if violations:
        df = pd.DataFrame([{
            "Date": v.get("violation_date", "")[:10],
            "Type": v.get("violation_type", ""),
            "Vehicle": v.get("vehicle_number", ""),
            "Fine (BDT)": v.get("fine_amount", 0),
            "Status": v.get("status", "")
        } for v in sorted(violations, key=lambda x: x.get("violation_date", ""), reverse=True)[:8]])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No violations on record.")

with col2:
    st.subheader("Recent Payments")
    if payments:
        df = pd.DataFrame([{
            "Date": p.get("payment_date", "")[:10],
            "Amount (BDT)": p.get("amount", 0),
            "Method": p.get("payment_method", ""),
            "Status": p.get("status", ""),
        } for p in sorted(payments, key=lambda x: x.get("payment_date", ""), reverse=True)[:8]])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No payments on record.")

st.divider()

# ---- Quick Links ----
st.subheader("Quick Links")
qc1, qc2, qc3, qc4 = st.columns(4)

with qc1:
    if st.button("🚙 Manage Vehicles", use_container_width=True):
        st.switch_page("pages/2_Vehicles.py")

with qc2:
    if st.button("🚨 View Violations", use_container_width=True):
        st.switch_page("pages/3_Violations.py")

with qc3:
    if st.button("💳 Make Payment", use_container_width=True):
        st.switch_page("pages/4_Payments.py")

with qc4:
    if st.button("📁 Document Vault", use_container_width=True):
        st.switch_page("pages/5_Documents.py")
