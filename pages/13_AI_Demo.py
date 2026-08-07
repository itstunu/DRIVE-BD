import streamlit as st
import auth
import random
import pandas as pd

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="AI Demo - DriveBD",
    page_icon="🤖",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()

# ---- Page Content ----
st.title("🤖 AI-Powered Features")

st.info("This page demonstrates AI-powered features for traffic violation detection and management.")

# ---- AI Features ----
tab1, tab2, tab3 = st.tabs(["📸 License Plate Detection", "🚗 Violation Detection", "💬 AI Chatbot"])

with tab1:
    st.subheader("📸 License Plate Recognition (Demo)")
    st.warning("This is a simulated demo. Upload an image to test.")
    
    uploaded_file = st.file_uploader("Upload vehicle image", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        with st.spinner("Processing image with AI..."):
            # Simulate AI processing
            st.image(uploaded_file, width=300)
            st.success("✅ License plate detected!")
            st.json({
                "license_plate": "BD-123-ABC",
                "confidence": "97.3%",
                "vehicle_make": random.choice(["Toyota", "Honda", "BMW"]),
                "vehicle_color": random.choice(["White", "Black", "Silver", "Blue"])
            })

with tab2:
    st.subheader("🚗 AI Violation Detection (Demo)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        violation_type = st.selectbox("Violation Type", [
            "Speeding",
            "Running Red Light",
            "Wrong Parking",
            "No Helmet",
            "Drink Driving"
        ])
    
    with col2:
        confidence = st.slider("AI Confidence Threshold", 50, 100, 80)
    
    if st.button("🚀 Run AI Detection"):
        with st.spinner("Analyzing with AI..."):
            detected = random.random() * 100 > confidence
            if detected:
                st.error(f"⚠️ Violation detected: **{violation_type}**")
                st.json({
                    "violation": violation_type,
                    "confidence": f"{random.randint(85, 99)}%",
                    "location": f"Lat: {random.uniform(23.7, 23.8):.4f}, Lon: {random.uniform(90.3, 90.4):.4f}",
                    "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                st.success("✅ No violation detected.")

with tab3:
    st.subheader("💬 AI Assistant (Simulated)")
    
    # Chat interface
    user_message = st.text_input("Ask me anything about traffic rules, violations, or vehicle registration...")
    
    if user_message:
        responses = [
            "Based on traffic rules, speeding fines range from $50 to $500 depending on the speed.",
            "You can appeal a violation within 30 days of receiving the ticket.",
            "Vehicle registration requires: NID, tax token, insurance, and fitness certificate.",
            "You can pay fines online using cash, card, or mobile banking.",
            "The BRTA issues driving licenses valid for 5 years."
        ]
        st.info(f"🤖 {random.choice(responses)}")