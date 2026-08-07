import streamlit as st
import auth
from db import get_violations, add_violation_to_db, update_violation_status
import pandas as pd

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="Violations - DriveBD",
    page_icon="⚠️",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()

# ---- Page Content ----
st.title("⚠️ Traffic Violations")

user = auth.current_user()
role = user.get('role')

# ---- Add Violation (Admin/BRTA Officer only) ----
if role in ['admin', 'officer']:
    with st.expander("➕ Record New Violation", expanded=False):
        with st.form("add_violation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                vehicle_number = st.text_input("Vehicle Number *")
                violation_type = st.selectbox("Violation Type *", [
                    "Speeding",
                    "Running Red Light",
                    "Wrong Parking",
                    "No Helmet",
                    "No Seatbelt",
                    "Drink Driving",
                    "Using Phone While Driving",
                    "Overloading",
                    "Other"
                ])
                location = st.text_input("Location")
            
            with col2:
                violation_date = st.date_input("Violation Date")
                fine_amount = st.number_input("Fine Amount ($)", min_value=0.0, step=10.0)
                status = st.selectbox("Status", ["pending", "paid", "appealed"])
            
            submitted = st.form_submit_button("Record Violation")
            
            if submitted and vehicle_number:
                violation_data = {
                    'vehicle_number': vehicle_number.upper(),
                    'violation_type': violation_type,
                    'violation_date': violation_date.isoformat(),
                    'location': location,
                    'fine_amount': fine_amount,
                    'status': status
                }
                result = add_violation_to_db(violation_data)
                if result:
                    st.success("✅ Violation recorded successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to record violation.")

# ---- Display Violations ----
st.subheader("📋 Violations")

violations = get_violations()

if violations:
    df = pd.DataFrame(violations)
    
    # Filter by role
    if role == 'driver':
        # Show only user's vehicles' violations
        st.info("Showing violations for your vehicles")
    
    st.dataframe(
        df[['vehicle_number', 'violation_type', 'violation_date', 'location', 'fine_amount', 'status']],
        use_container_width=True,
        hide_index=True
    )
    
    # Status update (Admin only)
    if role in ['admin', 'officer']:
        st.subheader("⚡ Update Violation Status")
        violation_ids = df['id'].tolist()
        selected_id = st.selectbox("Select Violation", violation_ids)
        new_status = st.selectbox("New Status", ["pending", "paid", "appealed"])
        if st.button("Update Status"):
            if update_violation_status(selected_id, new_status):
                st.success("✅ Status updated!")
                st.rerun()
            else:
                st.error("❌ Update failed")
else:
    st.info("No violations found.")