import streamlit as st
import auth
import random
import pandas as pd

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="Mock BRTA API - DriveBD",
    page_icon="🔌",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()

# ---- Page Content ----
st.title("🔌 Mock BRTA API Integration")

st.info("This page simulates integration with the Bangladesh Road Transport Authority (BRTA) API.")

# ---- API Simulation ----
st.subheader("📋 Vehicle Verification")

col1, col2 = st.columns(2)

with col1:
    reg_number = st.text_input("Enter Vehicle Registration Number", placeholder="e.g., BD-123-ABC")
    if st.button("🔍 Verify Vehicle"):
        if reg_number:
            # Simulate API call
            with st.spinner("Verifying with BRTA API..."):
                # Random verification result
                verified = random.choice([True, False])
                if verified:
                    st.success(f"✅ Vehicle **{reg_number.upper()}** verified successfully!")
                    st.json({
                        "registration": reg_number.upper(),
                        "make": random.choice(["Toyota", "Honda", "Nissan", "BMW", "Mercedes"]),
                        "model": random.choice(["Corolla", "Civic", "X-Trail", "X5", "E-Class"]),
                        "year": random.randint(2000, 2025),
                        "owner": "John Doe",
                        "tax_token": "Valid",
                        "insurance": "Valid",
                        "fitness": "Valid"
                    })
                else:
                    st.error(f"❌ Vehicle **{reg_number.upper()}** not found in BRTA database.")
        else:
            st.warning("Please enter a registration number.")

with col2:
    st.subheader("📋 License Verification")
    license_no = st.text_input("Enter License Number", placeholder="e.g., BD-12345")
    if st.button("🔍 Verify License"):
        if license_no:
            with st.spinner("Verifying with BRTA API..."):
                verified = random.choice([True, False])
                if verified:
                    st.success(f"✅ License **{license_no}** verified!")
                    st.json({
                        "license": license_no,
                        "name": "John Doe",
                        "class": random.choice(["A", "B", "C", "D"]),
                        "issue_date": "2020-01-01",
                        "expiry_date": "2025-01-01",
                        "status": "Valid"
                    })
                else:
                    st.error(f"❌ License **{license_no}** not found.")
        else:
            st.warning("Please enter a license number.")