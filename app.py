import streamlit as st
from db import init_db
import auth

st.set_page_config(
    page_title="DriveBD - Smart Driver & Vehicle Portal",
    page_icon="🚗",
    layout="wide"
)

init_db()

# ---- FORCE HIDE STREAMLIT'S AUTOMATIC SIDEBAR NAVIGATION ----
st.markdown("""
<style>
    /* Hide Streamlit's default page navigation */
    .stSidebarNav {
        display: none !important;
    }
    .stSidebar .st-emotion-cache-1v3fvcr {
        display: none !important;
    }
    .stSidebar .st-emotion-cache-1r6slb0 {
        display: none !important;
    }
    .stSidebar a[data-testid="stPageLink"] {
        display: none !important;
    }
    .stSidebar .st-emotion-cache-1wrcr25 {
        display: none !important;
    }
    .stSidebar .st-emotion-cache-1v3fvcr + div {
        display: none !important;
    }
    .stSidebar ul {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

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
        
        if "page" not in st.session_state:
            st.session_state.page = "Dashboard"
        
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
    left, right = st.columns([1.1, 1])
    with left:
        st.title("🚗 DriveBD")
        st.subheader("Smart Driver & Vehicle Owner Portal for Bangladesh")
        st.write("DriveBD is a unified portal for vehicle owners and drivers to manage registrations, traffic violations, fines, documents, service history and more.")
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
                if st.form_submit_button("Log In", use_container_width=True):
                    if auth.login(email, password):
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
        with tab_register:
            with st.form("register_form"):
                name = st.text_input("Full name")
                email = st.text_input("Email")
                phone = st.text_input("Phone number")
                nid = st.text_input("NID number")
                role = st.selectbox("Account type", ["driver", "owner"])
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Create Account", use_container_width=True):
                    if name and email and password:
                        ok, msg = auth.register_user(name, email, password, role, nid, phone)
                        st.success(msg) if ok else st.error(msg)
else:
    user = auth.current_user()
    page = st.session_state.page
    
    if page == "📊 Dashboard":
        st.title("📊 Dashboard")
        st.write(f"Welcome back, **{user['name']}**!")
        col1, col2, col3 = st.columns(3)
        col1.metric("🚗 Vehicles", "0")
        col2.metric("⚠️ Violations", "0")
        col3.metric("💰 Payments", "$0")
        st.divider()
        st.info("Use the sidebar to navigate to different modules.")
    
    elif page == "🚗 Vehicles":
        st.title("🚗 Vehicles")
        st.info("Vehicle management coming soon!")
    
    elif page == "⚠️ Violations":
        st.title("⚠️ Violations")
        st.info("Violation management coming soon!")
    
    elif page == "💰 Payments":
        st.title("💰 Payments")
        st.info("Payment processing coming soon!")
    
    elif page == "📄 Documents":
        st.title("📄 Documents")
        st.info("Document management coming soon!")
    
    elif page == "🔧 Service History":
        st.title("🔧 Service History")
        st.info("Service history coming soon!")
    
    elif page == "🔔 Notifications":
        st.title("🔔 Notifications")
        st.info("Notifications coming soon!")
    
    elif page == "⚖️ Appeals":
        st.title("⚖️ Appeals")
        st.info("Appeals coming soon!")
    
    elif page == "👑 Admin":
        if user['role'].lower() != 'admin':
            st.error("⚠️ Admin access only!")
        else:
            st.title("👑 Admin Panel")
            st.info("Admin panel coming soon!")
    
    elif page == "📈 Reports":
        st.title("📈 Reports")
        st.info("Reports coming soon!")
    
    elif page == "📉 Analytics":
        st.title("📉 Analytics")
        st.info("Analytics coming soon!")
    
    elif page == "🔌 Mock BRTA API":
        st.title("🔌 Mock BRTA API")
        st.info("BRTA API simulation coming soon!")
    
    elif page == "🤖 AI Demo":
        st.title("🤖 AI Demo")
        st.info("AI features coming soon!")

st.divider()
st.caption("DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data")
