import streamlit as st
from db import init_db
import auth
from db import get_vehicles, add_vehicle_to_db, get_violations, add_violation_to_db, get_payments, add_payment_to_db, get_documents, add_document_to_db, get_notifications, add_notification_to_db, get_appeals, add_appeal_to_db, update_violation_status
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="DriveBD - Smart Driver & Vehicle Portal",
    page_icon="🚗",
    layout="wide"
)

init_db()

# ---- HIDE STREAMLIT'S DEFAULT NAV ----
st.markdown("""
<style>
    .stSidebarNav { display: none !important; }
    .stSidebar .st-emotion-cache-1v3fvcr { display: none !important; }
    .stSidebar .st-emotion-cache-1r6slb0 { display: none !important; }
    .stSidebar a[data-testid="stPageLink"] { display: none !important; }
    .stSidebar .st-emotion-cache-1wrcr25 { display: none !important; }
    .stSidebar ul { display: none !important; }
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
    user_id = user.get('user_id')
    page = st.session_state.page
    
    # ========== DASHBOARD ==========
    if page == "📊 Dashboard":
        st.title("📊 Dashboard")
        st.write(f"Welcome back, **{user['name']}**!")
        
        vehicles = get_vehicles(user_id)
        violations = get_violations()
        payments = get_payments(user_id)
        notifications = get_notifications(user_id)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🚗 Vehicles", len(vehicles))
        pending = [v for v in violations if v.get('status') == 'pending']
        col2.metric("⚠️ Pending Violations", len(pending))
        unread = [n for n in notifications if not n.get('is_read', False)]
        col3.metric("🔔 Unread", len(unread))
        total_paid = sum([p.get('amount', 0) for p in payments if p.get('status') == 'completed'])
        col4.metric("💰 Paid", f"${total_paid:,.2f}")
        
        st.divider()
        if notifications:
            st.subheader("📋 Recent Activity")
            for n in notifications[:5]:
                st.info(f"🔔 **{n.get('title', '')}** - {n.get('message', '')}")
    
    # ========== VEHICLES ==========
    elif page == "🚗 Vehicles":
        st.title("🚗 Vehicle Management")
        
        with st.expander("➕ Register New Vehicle"):
            with st.form("add_vehicle"):
                col1, col2 = st.columns(2)
                with col1:
                    reg = st.text_input("Registration Number *")
                    make = st.text_input("Make *")
                    model = st.text_input("Model *")
                with col2:
                    year = st.number_input("Year", 1980, 2025, 2020)
                    color = st.text_input("Color")
                    status = st.selectbox("Status", ["active", "inactive"])
                if st.form_submit_button("Register"):
                    if reg and make and model:
                        data = {'user_id': user_id, 'registration_number': reg.upper(), 'make': make, 'model': model, 'year': year, 'color': color, 'status': status}
                        if add_vehicle_to_db(data):
                            st.success("✅ Registered!")
                            st.rerun()
                        else:
                            st.error("❌ Failed!")
        
        vehicles = get_vehicles(user_id)
        if vehicles:
            df = pd.DataFrame(vehicles)
            st.dataframe(df[['registration_number', 'make', 'model', 'year', 'color', 'status']], use_container_width=True, hide_index=True)
        else:
            st.info("No vehicles found.")
    
    # ========== VIOLATIONS ==========
    elif page == "⚠️ Violations":
        st.title("⚠️ Traffic Violations")
        
        if user['role'] in ['admin', 'officer']:
            with st.expander("➕ Record Violation"):
                with st.form("add_violation"):
                    col1, col2 = st.columns(2)
                    with col1:
                        vehicle = st.text_input("Vehicle Number *")
                        v_type = st.selectbox("Type", ["Speeding", "Running Red Light", "Wrong Parking", "No Helmet", "Drink Driving"])
                        location = st.text_input("Location")
                    with col2:
                        date = st.date_input("Date")
                        fine = st.number_input("Fine Amount ($)", 0.0, step=10.0)
                        status = st.selectbox("Status", ["pending", "paid", "appealed"])
                    if st.form_submit_button("Record"):
                        if vehicle:
                            data = {'vehicle_number': vehicle.upper(), 'violation_type': v_type, 'violation_date': date.isoformat(), 'location': location, 'fine_amount': fine, 'status': status}
                            if add_violation_to_db(data):
                                st.success("✅ Recorded!")
                                st.rerun()
        
        violations = get_violations()
        if violations:
            df = pd.DataFrame(violations)
            st.dataframe(df[['vehicle_number', 'violation_type', 'violation_date', 'fine_amount', 'status']], use_container_width=True, hide_index=True)
            
            if user['role'] in ['admin', 'officer']:
                st.subheader("Update Status")
                vid = st.selectbox("Select Violation", df['id'].tolist())
                new_status = st.selectbox("New Status", ["pending", "paid", "appealed"])
                if st.button("Update"):
                    if update_violation_status(vid, new_status):
                        st.success("✅ Updated!")
                        st.rerun()
        else:
            st.info("No violations found.")
    
    # ========== PAYMENTS ==========
    elif page == "💰 Payments":
        st.title("💰 Payment Management")
        
        with st.expander("💳 Make Payment"):
            violations = get_violations()
            pending = [v for v in violations if v.get('status') == 'pending']
            if pending:
                with st.form("pay"):
                    opts = {v['id']: f"{v['vehicle_number']} - ${v['fine_amount']}" for v in pending}
                    selected = st.selectbox("Select Violation", list(opts.keys()), format_func=lambda x: opts[x])
                    method = st.selectbox("Method", ["cash", "card", "mobile_banking"])
                    if st.form_submit_button("Pay Now"):
                        v = next(x for x in pending if x['id'] == selected)
                        data = {'violation_id': selected, 'user_id': user_id, 'amount': v['fine_amount'], 'payment_method': method, 'status': 'completed', 'transaction_id': f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}"}
                        if add_payment_to_db(data):
                            update_violation_status(selected, 'paid')
                            st.success(f"✅ Paid ${v['fine_amount']}!")
                            st.rerun()
            else:
                st.info("No pending violations.")
        
        payments = get_payments(user_id)
        if payments:
            df = pd.DataFrame(payments)
            st.dataframe(df[['amount', 'payment_date', 'payment_method', 'status', 'transaction_id']], use_container_width=True, hide_index=True)
            total = sum([p.get('amount', 0) for p in payments if p.get('status') == 'completed'])
            st.metric("💰 Total Paid", f"${total:,.2f}")
        else:
            st.info("No payments.")
    
    # ========== DOCUMENTS ==========
    elif page == "📄 Documents":
        st.title("📄 Document Management")
        
        with st.expander("📤 Upload Document"):
            with st.form("upload_doc"):
                name = st.text_input("Document Name *")
                doc_type = st.selectbox("Type", ["Registration", "Insurance", "Tax Token", "Pollution Certificate", "Fitness", "Other"])
                expiry = st.date_input("Expiry Date")
                file = st.file_uploader("Choose File", type=['pdf', 'jpg', 'png'])
                if st.form_submit_button("Upload"):
                    if name and file:
                        data = {'user_id': user_id, 'document_name': name, 'document_type': doc_type, 'file_url': file.name, 'expiry_date': expiry.isoformat(), 'verification_status': 'pending'}
                        if add_document_to_db(data):
                            st.success("✅ Uploaded!")
                            st.rerun()
        
        docs = get_documents(user_id)
        if docs:
            df = pd.DataFrame(docs)
            st.dataframe(df[['document_name', 'document_type', 'upload_date', 'expiry_date', 'verification_status']], use_container_width=True, hide_index=True)
        else:
            st.info("No documents.")
    
    # ========== SERVICE HISTORY ==========
    elif page == "🔧 Service History":
        st.title("🔧 Service History")
        st.info("📝 Service history tracking - add your service records here.")
        col1, col2, col3 = st.columns(3)
        col1.metric("🔧 Total Services", "0")
        col2.metric("📅 Last Service", "N/A")
        col3.metric("💰 Total Spent", "$0.00")
    
    # ========== NOTIFICATIONS ==========
    elif page == "🔔 Notifications":
        st.title("🔔 Notifications")
        notifs = get_notifications(user_id)
        if notifs:
            for n in notifs:
                if n.get('is_read', False):
                    st.markdown(f"**{n.get('title', '')}** - {n.get('message', '')}")
                else:
                    st.markdown(f"🔔 **{n.get('title', '')}** - {n.get('message', '')}")
                st.divider()
        else:
            st.info("📭 No notifications")
    
    # ========== APPEALS ==========
    elif page == "⚖️ Appeals":
        st.title("⚖️ Violation Appeals")
        
        with st.expander("📝 File Appeal"):
            violations = get_violations()
            pending = [v for v in violations if v.get('status') == 'pending']
            if pending:
                with st.form("appeal"):
                    opts = {v['id']: f"{v['vehicle_number']} - {v['violation_type']}" for v in pending}
                    selected = st.selectbox("Select Violation", list(opts.keys()), format_func=lambda x: opts[x])
                    reason = st.text_area("Reason *")
                    if st.form_submit_button("Submit"):
                        if reason:
                            data = {'violation_id': selected, 'user_id': user_id, 'reason': reason}
                            if add_appeal_to_db(data):
                                st.success("✅ Appeal submitted!")
                                st.rerun()
            else:
                st.info("No pending violations.")
        
        appeals = get_appeals(user_id)
        if appeals:
            df = pd.DataFrame(appeals)
            st.dataframe(df[['submission_date', 'reason', 'status', 'decision']], use_container_width=True, hide_index=True)
        else:
            st.info("No appeals.")
    
    # ========== ADMIN ==========
    elif page == "👑 Admin":
        if user['role'].lower() != 'admin':
            st.error("⚠️ Admin access only!")
        else:
            st.title("👑 Admin Panel")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("👤 Users", "0")
            col2.metric("🚗 Vehicles", len(get_vehicles()))
            col3.metric("⚠️ Violations", len(get_violations()))
            payments = get_payments()
            total = sum([p.get('amount', 0) for p in payments if p.get('status') == 'completed'])
            col4.metric("💰 Revenue", f"${total:,.2f}")
    
    # ========== REPORTS ==========
    elif page == "📈 Reports":
        st.title("📈 Reports")
        vehicles = get_vehicles()
        violations = get_violations()
        payments = get_payments()
        st.metric("🚗 Total Vehicles", len(vehicles))
        st.metric("⚠️ Total Violations", len(violations))
        total = sum([p.get('amount', 0) for p in payments if p.get('status') == 'completed'])
        st.metric("💰 Total Revenue", f"${total:,.2f}")
    
    # ========== ANALYTICS ==========
    elif page == "📉 Analytics":
        st.title("📉 Analytics")
        st.info("📊 Analytics dashboard coming with charts and graphs.")
        vehicles = get_vehicles()
        violations = get_violations()
        st.metric("🚗 Vehicles", len(vehicles))
        st.metric("⚠️ Violations", len(violations))
    
    # ========== MOCK BRTA API ==========
    elif page == "🔌 Mock BRTA API":
        st.title("🔌 Mock BRTA API")
        st.info("🔍 Simulate BRTA vehicle and license verification.")
        col1, col2 = st.columns(2)
        with col1:
            reg = st.text_input("Vehicle Number")
            if st.button("Verify Vehicle"):
                if reg:
                    st.json({"registration": reg.upper(), "make": "Toyota", "model": "Corolla", "year": 2020, "status": "Valid"})
        with col2:
            lic = st.text_input("License Number")
            if st.button("Verify License"):
                if lic:
                    st.json({"license": lic, "name": "John Doe", "class": "B", "status": "Valid"})
    
    # ========== AI DEMO ==========
    elif page == "🤖 AI Demo":
        st.title("🤖 AI Demo")
        st.info("🧠 AI-powered features demo.")
        tab1, tab2 = st.tabs(["📸 Plate Detection", "💬 Chatbot"])
        with tab1:
            st.warning("Upload an image to detect license plate.")
            uploaded = st.file_uploader("Choose Image", type=['jpg', 'png'])
            if uploaded:
                st.image(uploaded, width=200)
                st.success("✅ Plate detected: BD-123-ABC")
        with tab2:
            msg = st.text_input("Ask about traffic rules...")
            if msg:
                st.info("🤖 Response: Speeding fines range from $50 to $500.")

st.divider()
st.caption("DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data")
