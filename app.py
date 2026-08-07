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

# ---- Define Pages ----
def home_page():
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

# ---- Define Pages with st.Page ----
try:
    # Using st.navigation (Streamlit 1.36+)
    dashboard_page = st.Page("pages/1_Dashboard.py", title="Dashboard", icon="📊")
    vehicles_page = st.Page("pages/2_Vehicles.py", title="Vehicles", icon="🚗")
    violations_page = st.Page("pages/3_Violations.py", title="Violations", icon="🚨")
    payments_page = st.Page("pages/4_Payments.py", title="Payments", icon="💳")
    documents_page = st.Page("pages/5_Documents.py", title="Documents", icon="📄")
    service_page = st.Page("pages/6_Service_History.py", title="Service History", icon="🔧")
    notifications_page = st.Page("pages/7_Notifications.py", title="Notifications", icon="🔔")
    appeals_page = st.Page("pages/8_Appeals.py", title="Appeals", icon="⚖️")
    admin_page = st.Page("pages/9_Admin.py", title="Admin", icon="🛡️")
    reports_page = st.Page("pages/10_Reports.py", title="Reports", icon="📈")
    analytics_page = st.Page("pages/11_Analytics.py", title="Analytics", icon="📊")
    brta_page = st.Page("pages/12_Mock_BRTA_API.py", title="Mock BRTA API", icon="🏛️")
    ai_page = st.Page("pages/13_AI_Demo.py", title="AI Demo", icon="🤖")
    
    # Navigation
    pg = st.navigation({
        "Main": [dashboard_page, vehicles_page, violations_page, payments_page],
        "Records": [documents_page, service_page, notifications_page, appeals_page],
        "Admin": [admin_page, reports_page, analytics_page, brta_page, ai_page]
    })
    
    # Run the selected page
    pg.run()
    
except (AttributeError, TypeError):
    # Fallback for older Streamlit versions
    home_page()
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Navigation")
    st.sidebar.markdown("[📊 Dashboard](/1_Dashboard)")
    st.sidebar.markdown("[🚗 Vehicles](/2_Vehicles)")
    st.sidebar.markdown("[🚨 Violations](/3_Violations)")
    st.sidebar.markdown("[💳 Payments](/4_Payments)")
    st.sidebar.markdown("[📄 Documents](/5_Documents)")
    st.sidebar.markdown("[🔧 Service History](/6_Service_History)")
    st.sidebar.markdown("[🔔 Notifications](/7_Notifications)")
    st.sidebar.markdown("[⚖️ Appeals](/8_Appeals)")
    if auth.is_logged_in() and auth.current_user()['role'].lower() == 'admin':
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔐 Admin")
        st.sidebar.markdown("[🛡️ Admin Panel](/9_Admin)")
        st.sidebar.markdown("[📈 Reports](/10_Reports)")
        st.sidebar.markdown("[📊 Analytics](/11_Analytics)")
        st.sidebar.markdown("[🏛️ Mock BRTA API](/12_Mock_BRTA_API)")
        st.sidebar.markdown("[🤖 AI Demo](/13_AI_Demo)")
