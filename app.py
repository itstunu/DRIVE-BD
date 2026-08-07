import streamlit as st
from db import init_db
import auth

# ---- MUST BE FIRST ----
st.set_page_config(
    page_title="DriveBD - Smart Driver & Vehicle Portal",
    page_icon="🚗",
    layout="wide"
)

# ---- Initialize Database ----
init_db()

# ---- Sidebar ----
with st.sidebar:
    st.markdown("### 🚗 DriveBD")
    st.markdown("---")
    
    if auth.is_logged_in():
        user = auth.current_user()
        st.markdown(f"👤 **{user['name']}**")
        st.markdown(f"📧 {user['email']}")
        st.markdown(f"🔑 Role: **{user['role'].title()}**")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout()
            st.rerun()
    else:
        st.info("👈 Please log in")

# ---- MAIN CONTENT ----
if auth.is_logged_in():
    user = auth.current_user()
    st.markdown("### 🚗 DriveBD")
    st.markdown("Smart Driver & Vehicle Owner Portal")
    st.success(f"Logged in as **{user['name']}** ({user['role'].title()})")
    st.info("👈 Use the sidebar to navigate to different modules.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Role", user['role'].title())
    with col2:
        st.metric("Email", user['email'])
    with col3:
        st.metric("User ID", user['user_id'][:8] + "...")
    
    st.divider()
    st.subheader("Quick Actions")
    
    # Use st.page_link (works in newer Streamlit)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.page_link("pages/1_Dashboard.py", label="📊 Dashboard", icon="📊")
    with col2:
        st.page_link("pages/2_Vehicles.py", label="🚗 Vehicles", icon="🚗")
    with col3:
        st.page_link("pages/3_Violations.py", label="🚨 Violations", icon="🚨")
    with col4:
        st.page_link("pages/4_Payments.py", label="💳 Payments", icon="💳")
    
    # Second row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.page_link("pages/5_Documents.py", label="📄 Documents", icon="📄")
    with col2:
        st.page_link("pages/6_Service_History.py", label="🔧 Service", icon="🔧")
    with col3:
        st.page_link("pages/7_Notifications.py", label="🔔 Notifications", icon="🔔")
    with col4:
        st.page_link("pages/8_Appeals.py", label="⚖️ Appeals", icon="⚖️")
else:
    # ---- LOGIN PAGE ----
    left, right = st.columns([1.1, 1])
    with left:
        st.markdown("### 🚗 DriveBD")
        st.markdown("Smart Driver & Vehicle Owner Portal for Bangladesh")
        st.write("""
        DriveBD is a unified portal for vehicle owners and drivers to manage registrations,
        traffic violations, fines, documents, service history and more.
        """)
        st.markdown("""
        **Demo accounts:**
        - 👤 Owner demo: `demo@drivebd.gov.bd` / `Demo@123`
        - 🛡️ Admin demo: `admin@drivebd.gov.bd` / `Admin@123`
        """)

    with right:
        tab_login, tab_register = st.tabs(["Log In", "Create Account"])

        with tab_login:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Log In")
                if submitted:
                    if auth.login(email, password):
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

        with tab_register:
            with st.form("register_form"):
                name = st.text_input("Full name")
                email_r = st.text_input("Email", key="reg_email")
                phone = st.text_input("Phone number")
                nid = st.text_input("NID number")
                role = st.selectbox("Account type", ["driver", "owner"])
                password_r = st.text_input("Password", type="password", key="reg_pw")
                submitted_r = st.form_submit_button("Create Account")
                if submitted_r:
                    if not (name and email_r and password_r):
                        st.error("Name, email and password are required.")
                    else:
                        ok, msg = auth.register_user(name, email_r, password_r, role, nid=nid, phone=phone)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)

st.divider()
st.caption("DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data")
