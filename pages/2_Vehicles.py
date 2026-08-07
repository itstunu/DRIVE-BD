import streamlit as st
import auth
from db import get_vehicles, add_vehicle_to_db
import pandas as pd

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="Vehicles - DriveBD",
    page_icon="🚗",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()

# ---- Page Content ----
st.title("🚗 Vehicle Management")

user = auth.current_user()
user_id = user.get('user_id')

# ---- Add Vehicle Form ----
with st.expander("➕ Register New Vehicle", expanded=False):
    with st.form("add_vehicle_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            reg_number = st.text_input("Registration Number *", placeholder="e.g., BD-123-ABC")
            make = st.text_input("Make *", placeholder="e.g., Toyota")
            model = st.text_input("Model *", placeholder="e.g., Corolla")
            year = st.number_input("Year", min_value=1980, max_value=2025, value=2020)
        
        with col2:
            color = st.text_input("Color", placeholder="e.g., White")
            chassis = st.text_input("Chassis Number", placeholder="e.g., 1HGCM82633A123456")
            engine = st.text_input("Engine Number", placeholder="e.g., EN123456789")
            status = st.selectbox("Status", ["active", "inactive", "suspended"])
        
        submitted = st.form_submit_button("Register Vehicle")
        
        if submitted:
            if not reg_number or not make or not model:
                st.error("Registration Number, Make and Model are required!")
            else:
                vehicle_data = {
                    'user_id': user_id,
                    'registration_number': reg_number.upper(),
                    'make': make,
                    'model': model,
                    'year': year,
                    'color': color,
                    'chassis_number': chassis,
                    'engine_number': engine,
                    'status': status
                }
                result = add_vehicle_to_db(vehicle_data)
                if result:
                    st.success("✅ Vehicle registered successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to register vehicle. Registration number may already exist.")

# ---- Display Vehicles ----
st.subheader("📋 Your Vehicles")

vehicles = get_vehicles(user_id)

if vehicles:
    df = pd.DataFrame(vehicles)
    st.dataframe(
        df[['registration_number', 'make', 'model', 'year', 'color', 'status']],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No vehicles registered yet. Use the form above to add one.")