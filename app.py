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
        
        st.markdown("**app**")
        
        # Store current page in session state
        if "page" not in st.session_state:
            st.session_state.page = "Dashboard"
        
        # Navigation buttons
        pages = [
            "📊 Dashboard",
            "🚗 Vehicles",
            "⚠️ Violations",
            "💰 Payments",
            "📄 Documents",
            "🔧 Service History",
            "🔔 Notifications",
            "⚖️ Appeals",
            "👑 Admin",
            "📈 Reports",
            "📉 Analytics",
            "🔌 Mock BRTA API",
            "🤖 AI Demo"
        ]
        
        for p in pages:
            # Highlight active page
            if st.session_state.page == p:
                st.button(f"✅ {p}", key=p, use_container_width=True)
            else:
                if st.button(p, key=p, use_container_width=True):
                    st.session_state.page = p
                    st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout()
            st.session_state.page = "Dashboard"
            st.rerun()
    else:
        st.info("👋 Please log in")

# ---- MAIN CONTENT ----
if not auth.is_logged_in():
    # ---- LOGIN PAGE ----
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
    page = st.session_state.page
    
    if page == "📊 Dashboard":
        st.title("📊 Dashboard")
        st.write(f"Welcome back, **{user['name']}**!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🚗 Vehicles", "0")
        with col2:
            st.metric("⚠️ Violations", "0")
        with col3:
            st.metric("💰 Payments", "$0")
        
        st.divider()
        st.info("Use the sidebar to navigate to different modules.")
    
    elif page == "🚗 Vehicles":
        st.title("🚗 Vehicles")
        st.write("Manage your vehicles here.")
        st.info("Vehicle management feature coming soon!")
    
    elif page == "⚠️ Violations":
        st.title("⚠️ Violations")
        st.write("View and manage traffic violations.")
        st.info("Violation management feature coming soon!")
    
    elif page == "💰 Payments":
        st.title("💰 Payments")
        st.write("Make payments for violations.")
        st.info("Payment processing feature coming soon!")
    
    elif page == "📄 Documents":
        st.title("📄 Documents")
        st.write("Upload and manage your documents.")
        st.info("Document management feature coming soon!")
    
    elif page == "🔧 Service History":
        st.title("🔧 Service History")
        st.write("Track your vehicle service history.")
        st.info("Service history feature coming soon!")
    
    elif page == "🔔 Notifications":
        st.title("🔔 Notifications")
        st.write("View your notifications.")
        st.info("Notifications feature coming soon!")
    
    elif page == "⚖️ Appeals":
        st.title("⚖️ Appeals")
        st.write("File appeals for violations.")
        st.info("Appeals management feature coming soon!")
    
    elif page == "👑 Admin":
        st.title("👑 Admin Panel")
        if user['role'].lower() != 'admin':
            st.error("⚠️ You need Admin privileges to access this page.")
        else:
            st.write("Administrative controls.")
            st.info("Admin panel coming soon!")
    
    elif page == "📈 Reports":
        st.title("📈 Reports")
        st.write("Generate and view reports.")
        st.info("Reports feature coming soon!")
    
    elif page == "📉 Analytics":
        st.title("📉 Analytics")
        st.write("View analytics and insights.")
        st.info("Analytics feature coming soon!")
    
    elif page == "🔌 Mock BRTA API":
        st.title("🔌 Mock BRTA API")
        st.write("Simulate BRTA API integration.")
        st.info("BRTA API simulation coming soon!")
    
    elif page == "🤖 AI Demo":
        st.title("🤖 AI Demo")
        st.write("AI-powered features demo.")
        st.info("AI features coming soon!")

st.divider()
st.caption("DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data")
