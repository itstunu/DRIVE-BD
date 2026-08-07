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

# ---- Custom CSS for Sidebar ----
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #0e1f3a;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    .sidebar-header {
        color: white !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        padding: 1rem 0 0.3rem 0 !important;
        border-bottom: 1px solid rgba(255,255,255,0.1) !important;
        margin-bottom: 0.5rem !important;
    }
    
    .sidebar-subheader {
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.7rem !important;
        text-align: center !important;
        padding-bottom: 1rem !important;
        border-bottom: 1px solid rgba(255,255,255,0.05) !important;
    }
    
    .user-card {
        background: rgba(255,255,255,0.08);
        padding: 12px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .user-name {
        color: white !important;
        margin: 0 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }
    
    .user-role {
        color: rgba(255,255,255,0.5) !important;
        margin: 0 !important;
        font-size: 0.75rem !important;
    }
    
    /* Main header */
    .main-header {
        font-size: 2.4rem;
        font-weight: 700;
        color: #0B5FFF;
        margin-bottom: 0;
    }
    
    .sub-header {
        color: #555;
        font-size: 1.05rem;
        margin-top: 0;
    }
    
    .metric-card {
        background: #F0F5FF;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #D6E4FF;
    }
    
    div.stButton > button {
        background-color: #0B5FFF;
        color: white;
        border-radius: 8px;
        border: none;
    }
    
    div.stButton > button:hover {
        background-color: #0847C4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ---- SIDEBAR ----
with st.sidebar:
    # App Header
    st.markdown('<p class="sidebar-header">🚗 DriveBD</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-subheader">Smart Driver & Vehicle Portal</p>', unsafe_allow_html=True)
    
    if auth.is_logged_in():
        user = auth.current_user()
        
        # User info
        st.markdown(f"""
        <div class="user-card">
            <p class="user-name">👤 {user['name']}</p>
            <p class="user-role">{user['role'].title()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout()
            st.rerun()
    else:
        st.info("👋 Please log in")
        
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; margin: 10px 0;">
            <p style="color: rgba(255,255,255,0.5); margin: 0; font-size: 0.7rem;">
            🔑 demo@drivebd.gov.bd<br>
            🔑 admin@drivebd.gov.bd
            </p>
        </div>
        """, unsafe_allow_html=True)

# ---- MAIN APP ----
if auth.is_logged_in():
    user = auth.current_user()
    st.markdown('<p class="main-header">🚗 DriveBD</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Smart Driver & Vehicle Owner Portal</p>', unsafe_allow_html=True)
    st.success(f"Logged in as **{user['name']}** ({user['role'].title()})")
    st.info("Use the sidebar to navigate to Dashboard, Vehicles, Violations, Payments and other modules.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><b>📋 Role</b><br>{user["role"].title()}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><b>📧 Email</b><br>{user["email"]}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><b>✅ Status</b><br>Active</div>', unsafe_allow_html=True)
else:
    left, right = st.columns([1.1, 1])
    with left:
        st.markdown('<p class="main-header">🚗 DriveBD</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Smart Driver & Vehicle Owner Portal for Bangladesh</p>', unsafe_allow_html=True)
        st.write("""
        DriveBD is a unified portal for vehicle owners and drivers to manage registrations,
        traffic violations, fines, documents, service history and more — with a mock BRTA
        integration and a demo AI violation detector.
        """)
        st.markdown("""
        **Demo accounts (pre-seeded):**
        - 👤 Owner demo: `demo@drivebd.gov.bd` / `Demo@123`
        - 🛡️ Admin demo: `admin@drivebd.gov.bd` / `Admin@123`
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

st.divider()
st.caption("DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data")
