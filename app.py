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

# ---- HIDE ONLY "VIEW LESS" AND SIDEBAR TITLE ----
st.markdown("""
<style>
    /* Hide "View less" button */
    .stSidebar button[kind="secondary"] {
        display: none !important;
    }
    
    /* Hide sidebar title (DriveBD) */
    .stSidebar > div:first-child > div:first-child {
        display: none !important;
    }
    
    /* Hide Streamlit's default navigation */
    .stSidebarNav {
        display: none !important;
    }
    .stSidebar .st-emotion-cache-1r6slb0 {
        display: none !important;
    }
    .stSidebar .st-emotion-cache-1v3fvcr {
        display: none !important;
    }
    .stSidebar .stPageLink {
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
    .stSidebar a[data-testid="stPageLink"] {
        display: none !important;
    }
    .stSidebar .st-emotion-cache-16idsys {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ---- SIDEBAR ----
with st.sidebar:
    # NO TITLE - just the menu
    st.markdown("**app**")
    
    pages = {
        "📊 Dashboard": "1_Dashboard",
        "🚗 Vehicles": "2_Vehicles",
        "⚠️ Violations": "3_Violations",
        "💰 Payments": "4_Payments",
        "📄 Documents": "5_Documents",
        "🔧 Service History": "6_Service_History",
        "🔔 Notifications": "7_Notifications",
        "⚖️ Appeals": "8_Appeals",
        "👑 Admin": "9_Admin",
        "📈 Reports": "10_Reports",
        "📉 Analytics": "11_Analytics",
        "🔌 Mock BRTA API": "12_Mock_BRTA_API",
        "🤖 AI Demo": "13_AI_Demo"
    }
    
    for label, page in pages.items():
        if st.button(label, key=page, use_container_width=True):
            st.switch_page(f"pages/{page}.py")
    
    st.markdown("---")
    
    if st.button("🚪 Logout", use_container_width=True):
        auth.logout()
        st.rerun()

# ---- MAIN APP ----
if auth.is_logged_in():
    user = auth.current_user()
    
    st.title("🚗 DriveBD")
    st.subheader("Smart Driver & Vehicle Owner Portal")
    st.success(f"Logged in as **{user['name']}** ({user['role'].title()})")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background:#f0f2f6; padding:15px; border-radius:10px; text-align:center;">
            <p style="font-size:12px; color:#888; margin:0;">📋 ROLE</p>
            <p style="font-size:18px; font-weight:bold; margin:5px 0 0 0;">{user['role'].title()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background:#f0f2f6; padding:15px; border-radius:10px; text-align:center;">
            <p style="font-size:12px; color:#888; margin:0;">📧 EMAIL</p>
            <p style="font-size:14px; font-weight:bold; margin:5px 0 0 0; word-break:break-all;">{user['email']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background:#f0f2f6; padding:15px; border-radius:10px; text-align:center;">
            <p style="font-size:12px; color:#888; margin:0;">✅ STATUS</p>
            <p style="font-size:18px; font-weight:bold; margin:5px 0 0 0; color:#00C853;">Active</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.info("Use the sidebar to navigate to Dashboard, Vehicles, Violations, Payments and other modules.")

else:
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

st.divider()
st.caption("DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data")
