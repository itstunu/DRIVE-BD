import streamlit as st
from db import init_db
import auth

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="DriveBD - Smart Driver & Vehicle Portal",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Initialize Database ----
init_db()

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("### 🚗 DriveBD")
    st.markdown("Smart Driver & Vehicle Portal")
    st.markdown("---")
    
    if auth.is_logged_in():
        user = auth.current_user()
        st.markdown(f"👤 **{user['name']}**")
        st.markdown(f"*{user['role'].title()}*")
        st.markdown("---")
        
        # ---- Create navigation menu ----
        st.markdown("**app**")
        
        # Define pages with their display names and icons
        pages = {
            "📊 Dashboard": "dashboard",
            "🚗 Vehicles": "vehicles",
            "⚠️ Violations": "violations",
            "💰 Payments": "payments",
            "📄 Documents": "documents",
            "🔧 Service History": "service_history",
            "🔔 Notifications": "notifications",
            "⚖️ Appeals": "appeals",
            "👑 Admin": "admin",
            "📈 Reports": "reports",
            "📉 Analytics": "analytics",
            "🔌 Mock BRTA API": "mock_brta_api",
            "🤖 AI Demo": "ai_demo"
        }
        
        # Store selected page in session state
        if "selected_page" not in st.session_state:
            st.session_state.selected_page = "dashboard"
        
        for label, page_id in pages.items():
            # Highlight active page
            button_style = "primary" if st.session_state.selected_page == page_id else "secondary"
            if st.button(label, key=page_id, use_container_width=True, type=button_style):
                st.session_state.selected_page = page_id
                st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout()
            st.session_state.selected_page = "dashboard"
            st.rerun()
    else:
        st.info("👋 Please log in")

# ---- PAGE CONTENT ----
if not auth.is_logged_in():
    # Show login page
    left, right = st.columns([1.1, 1])
    with left:
        st.title("🚗 DriveBD")
        st.subheader("Smart Driver & Vehicle Owner Portal for Bangladesh")
        st.write("""
        DriveBD is a unified portal for vehicle owners and drivers to manage registrations,
        traffic violations, fines, documents, service history and more.
        """)
        st.markdown("""
        **Demo accounts:**
        - 👤 Owner: `demo@drivebd.gov.bd` / `Demo@123`
        - 🛡️ Admin: `admin@drivebd.gov.bd` / `Admin@123`
        """)

    with right:
        tab_login, tab_register = st.tabs(["🔐 Log In", "📝 Create Account"])

        with tab_login:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Log In", use_container_width=True)
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
                submitted_r = st.form_submit_button("Create Account", use_container_width=True)
                if submitted_r:
                    if not (name and email_r and password_r):
                        st.error("Name, email and password are required.")
                    else:
                        ok, msg = auth.register_user(name, email_r, password_r, role, nid=nid, phone=phone)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)
else:
    # ---- SHOW SELECTED PAGE ----
    user = auth.current_user()
    selected = st.session_state.selected_page
    
    if selected == "dashboard":
        st.title("📊 Dashboard")
        st.write(f"Welcome back, **{user['name']}**!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🚗 Vehicles", "0")
        with col2:
            st.metric("⚠️ Violations", "0")
        with col3:
            st.metric("💰 Payments", "$0")
    
    elif selected == "vehicles":
        st.title("🚗 Vehicles")
        st.write("Manage your vehicles here.")
        st.info("Vehicle management coming soon!")
    
    elif selected == "violations":
        st.title("⚠️ Violations")
        st.write("View and manage traffic violations.")
        st.info("Violation management coming soon!")
    
    elif selected == "payments":
        st.title("💰 Payments")
        st.write("Make payments for violations.")
        st.info("Payment processing coming soon!")
    
    elif selected == "documents":
        st.title("📄 Documents")
        st.write("Upload and manage your documents.")
        st.info("Document management coming soon!")
    
    elif selected == "service_history":
        st.title("🔧 Service History")
        st.write("Track your vehicle service history.")
        st.info("Service history coming soon!")
    
    elif selected == "notifications":
        st.title("🔔 Notifications")
        st.write("View your notifications.")
        st.info("Notifications coming soon!")
    
    elif selected == "appeals":
        st.title("⚖️ Appeals")
        st.write("File appeals for violations.")
        st.info("Appeals management coming soon!")
    
    elif selected == "admin":
        st.title("👑 Admin Panel")
        st.write("Administrative controls.")
        if user['role'].lower() != 'admin':
            st.error("⚠️ You need Admin privileges to access this page.")
        else:
            st.info("Admin panel coming soon!")
    
    elif selected == "reports":
        st.title("📈 Reports")
        st.write("Generate and view reports.")
        st.info("Reports coming soon!")
    
    elif selected == "analytics":
        st.title("📉 Analytics")
        st.write("View analytics and insights.")
        st.info("Analytics coming soon!")
    
    elif selected == "mock_brta_api":
        st.title("🔌 Mock BRTA API")
        st.write("Simulate BRTA API integration.")
        st.info("BRTA API simulation coming soon!")
    
    elif selected == "ai_demo":
        st.title("🤖 AI Demo")
        st.write("AI-powered features demo.")
        st.info("AI features coming soon!")

st.divider()
st.caption("DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data")
