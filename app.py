import streamlit as st
from db import init_db
import auth
from db import get_vehicles, add_vehicle_to_db, get_violations, add_violation_to_db, get_payments, add_payment_to_db, get_documents, add_document_to_db, get_notifications, add_notification_to_db, get_appeals, add_appeal_to_db, update_violation_status
import pandas as pd
from datetime import datetime

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="DriveBD - Smart Driver & Vehicle Portal",
    page_icon="🚗",
    layout="wide"
)

init_db()

# ---- HIDE STREAMLIT DEFAULT NAV ----
st.markdown("""
<style>
    .stSidebarNav { display: none !important; }
    .stSidebar .st-emotion-cache-1v3fvcr { display: none !important; }
    .stSidebar .st-emotion-cache-1r6slb0 { display: none !important; }
    .stSidebar a[data-testid="stPageLink"] { display: none !important; }
    .stSidebar ul { display: none !important; }
    .stSidebar .st-emotion-cache-1wrcr25 { display: none !important; }
    .stSidebar button[kind="secondary"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
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

# ============================================================
# MAIN CONTENT
# ============================================================
if not auth.is_logged_in():
    # ---- FRONT PAGE / LOGIN ----
    st.title("🚗 DriveBD")
    st.subheader("Smart Driver & Vehicle Owner Portal for Bangladesh")
    st.write("Manage registrations, violations, payments, documents, and service history.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Demo Accounts:**
        - 👤 Owner: `demo@drivebd.gov.bd` / `Demo@123`
        - 🛡️ Admin: `admin@drivebd.gov.bd` / `Admin@123`
        """)
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", use_container_width=True)
                if submitted:
                    if auth.login(email, password):
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
        with tab2:
            with st.form("register_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                nid = st.text_input("NID")
                role = st.selectbox("Role", ["driver", "owner"])
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Create Account", use_container_width=True)
                if submitted:
                    if name and email and password:
                        ok, msg = auth.register_user(name, email, password, role, nid, phone)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)
    
    st.divider()
    st.caption("DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data")

else:
    # ============================================================
    # ALL MODULES (Logged In)
    # ============================================================
    user = auth.current_user()
    user_id = user.get('user_id')
    page = st.session_state.page

    # ---- DASHBOARD ----
    if page == "📊 Dashboard":
        st.title("📊 Dashboard")
        st.write(f"Welcome back, **{user['name']}**!")

        vehicles = get_vehicles(user_id)
        violations = get_violations()
        payments = get_payments(user_id)
        notifications = get_notifications(user_id)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🚗 Vehicles", len(vehicles))
        pending = [v for v in violations if v.get('status') == 'pending']
        c2.metric("⚠️ Pending Violations", len(pending))
        unread = [n for n in notifications if not n.get('is_read', False)]
        c3.metric("🔔 Unread", len(unread))
        total_paid = sum(p.get('amount', 0) for p in payments if p.get('status') == 'completed')
        c4.metric("💰 Paid", f"${total_paid:,.2f}")

        if notifications:
            st.divider()
            st.subheader("📋 Recent Activity")
            for n in notifications[:5]:
                st.info(f"🔔 {n.get('title', '')} - {n.get('message', '')}")

    # ---- VEHICLES ----
    elif page == "🚗 Vehicles":
        st.title("🚗 Vehicle Management")
        with st.expander("➕ Register New Vehicle"):
            with st.form("add_vehicle"):
                c1, c2 = st.columns(2)
                with c1:
                    reg = st.text_input("Registration *")
                    make = st.text_input("Make *")
                    model = st.text_input("Model *")
                with c2:
                    year = st.number_input("Year", 1980, 2025, 2020)
                    color = st.text_input("Color")
                    status = st.selectbox("Status", ["active", "inactive"])
                if st.form_submit_button("Register"):
                    if reg and make and model:
                        data = {
                            'user_id': user_id,
                            'registration_number': reg.upper(),
                            'make': make,
                            'model': model,
                            'year': year,
                            'color': color,
                            'status': status
                        }
                        if add_vehicle_to_db(data):
                            st.success("✅ Registered!")
                            st.rerun()
                        else:
                            st.error("❌ Failed")
        vehicles = get_vehicles(user_id)
        if vehicles:
            df = pd.DataFrame(vehicles)
            st.dataframe(df[['registration_number','make','model','year','color','status']], use_container_width=True, hide_index=True)
        else:
            st.info("No vehicles.")

    # ---- VIOLATIONS ----
    elif page == "⚠️ Violations":
        st.title("⚠️ Traffic Violations")
        if user['role'] in ['admin','officer']:
            with st.expander("➕ Record Violation"):
                with st.form("add_violation"):
                    c1, c2 = st.columns(2)
                    with c1:
                        vehicle = st.text_input("Vehicle *")
                        vtype = st.selectbox("Type", ["Speeding","Red Light","Wrong Parking","No Helmet","Drink Driving"])
                        loc = st.text_input("Location")
                    with c2:
                        date = st.date_input("Date")
                        fine = st.number_input("Fine ($)", 0.0, step=10.0)
                        status = st.selectbox("Status", ["pending","paid","appealed"])
                    if st.form_submit_button("Record"):
                        if vehicle:
                            data = {
                                'vehicle_number': vehicle.upper(),
                                'violation_type': vtype,
                                'violation_date': date.isoformat(),
                                'location': loc,
                                'fine_amount': fine,
                                'status': status
                            }
                            if add_violation_to_db(data):
                                st.success("✅ Recorded!")
                                st.rerun()
        violations = get_violations()
        if violations:
            df = pd.DataFrame(violations)
            st.dataframe(df[['vehicle_number','violation_type','violation_date','fine_amount','status']], use_container_width=True, hide_index=True)
            if user['role'] in ['admin','officer']:
                st.subheader("Update Status")
                vid = st.selectbox("Select Violation", df['id'].tolist())
                ns = st.selectbox("New Status", ["pending","paid","appealed"])
                if st.button("Update"):
                    if update_violation_status(vid, ns):
                        st.success("✅ Updated!")
                        st.rerun()
        else:
            st.info("No violations.")

    # ---- PAYMENTS ----
    elif page == "💰 Payments":
        st.title("💰 Payment Management")
        with st.expander("💳 Make Payment"):
            violations = get_violations()
            pending = [v for v in violations if v.get('status') == 'pending']
            if pending:
                with st.form("pay"):
                    opts = {v['id']: f"{v['vehicle_number']} - ${v['fine_amount']}" for v in pending}
                    sel = st.selectbox("Violation", list(opts.keys()), format_func=lambda x: opts[x])
                    method = st.selectbox("Method", ["cash","card","mobile"])
                    if st.form_submit_button("Pay Now"):
                        v = next(x for x in pending if x['id'] == sel)
                        data = {
                            'violation_id': sel,
                            'user_id': user_id,
                            'amount': v['fine_amount'],
                            'payment_method': method,
                            'status': 'completed',
                            'transaction_id': f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                        }
                        if add_payment_to_db(data):
                            update_violation_status(sel, 'paid')
                            st.success(f"✅ Paid ${v['fine_amount']}!")
                            st.rerun()
            else:
                st.info("No pending violations.")
        payments = get_payments(user_id)
        if payments:
            df = pd.DataFrame(payments)
            st.dataframe(df[['amount','payment_date','payment_method','status','transaction_id']], use_container_width=True, hide_index=True)
            total = sum(p.get('amount',0) for p in payments if p.get('status')=='completed')
            st.metric("💰 Total Paid", f"${total:,.2f}")
        else:
            st.info("No payments.")

    # ---- DOCUMENTS ----
    elif page == "📄 Documents":
        st.title("📄 Document Management")
        with st.expander("📤 Upload"):
            with st.form("upload_doc"):
                name = st.text_input("Name *")
                dtype = st.selectbox("Type", ["Registration","Insurance","Tax Token","Pollution","Fitness","Other"])
                expiry = st.date_input("Expiry")
                file = st.file_uploader("File", type=['pdf','jpg','png'])
                if st.form_submit_button("Upload"):
                    if name and file:
                        data = {
                            'user_id': user_id,
                            'document_name': name,
                            'document_type': dtype,
                            'file_url': file.name,
                            'expiry_date': expiry.isoformat(),
                            'verification_status': 'pending'
                        }
                        if add_document_to_db(data):
                            st.success("✅ Uploaded!")
                            st.rerun()
        docs = get_documents(user_id)
        if docs:
            df = pd.DataFrame(docs)
            st.dataframe(df[['document_name','document_type','upload_date','expiry_date','verification_status']], use_container_width=True, hide_index=True)
        else:
            st.info("No documents.")

    # ---- SERVICE HISTORY ----
    elif page == "🔧 Service History":
        st.title("🔧 Service History")
        st.info("Service records will appear here.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Services", "0")
        c2.metric("Last Service", "N/A")
        c3.metric("Total Spent", "$0")

    # ---- NOTIFICATIONS ----
    elif page == "🔔 Notifications":
        st.title("🔔 Notifications")
        notifs = get_notifications(user_id)
        if notifs:
            for n in notifs:
                st.markdown(f"**{n.get('title','')}** - {n.get('message','')}")
                st.divider()
        else:
            st.info("No notifications.")

    # ---- APPEALS ----
    elif page == "⚖️ Appeals":
        st.title("⚖️ Appeals")
        with st.expander("📝 File Appeal"):
            violations = get_violations()
            pending = [v for v in violations if v.get('status') == 'pending']
            if pending:
                with st.form("appeal"):
                    opts = {v['id']: f"{v['vehicle_number']} - {v['violation_type']}" for v in pending}
                    sel = st.selectbox("Violation", list(opts.keys()), format_func=lambda x: opts[x])
                    reason = st.text_area("Reason *")
                    if st.form_submit_button("Submit"):
                        if reason:
                            data = {'violation_id': sel, 'user_id': user_id, 'reason': reason}
                            if add_appeal_to_db(data):
                                st.success("✅ Submitted!")
                                st.rerun()
            else:
                st.info("No pending violations.")
        appeals = get_appeals(user_id)
        if appeals:
            df = pd.DataFrame(appeals)
            st.dataframe(df[['submission_date','reason','status','decision']], use_container_width=True, hide_index=True)
        else:
            st.info("No appeals.")

    # ---- ADMIN ----
    elif page == "👑 Admin":
        if user['role'].lower() != 'admin':
            st.error("⚠️ Admin only!")
        else:
            st.title("👑 Admin Panel")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Users", "0")
            c2.metric("Vehicles", len(get_vehicles()))
            c3.metric("Violations", len(get_violations()))
            total = sum(p.get('amount',0) for p in get_payments() if p.get('status')=='completed')
            c4.metric("Revenue", f"${total:,.2f}")

    # ---- REPORTS ----
    elif page == "📈 Reports":
        st.title("📈 Reports")
        c1, c2, c3 = st.columns(3)
        c1.metric("Vehicles", len(get_vehicles()))
        c2.metric("Violations", len(get_violations()))
        total = sum(p.get('amount',0) for p in get_payments() if p.get('status')=='completed')
        c3.metric("Revenue", f"${total:,.2f}")

    # ---- ANALYTICS ----
    elif page == "📉 Analytics":
        st.title("📉 Analytics")
        st.info("Charts coming soon.")
        c1, c2 = st.columns(2)
        c1.metric("Vehicles", len(get_vehicles()))
        c2.metric("Violations", len(get_violations()))

    # ---- MOCK BRTA ----
    elif page == "🔌 Mock BRTA API":
        st.title("🔌 Mock BRTA API")
        c1, c2 = st.columns(2)
        with c1:
            reg = st.text_input("Vehicle Number")
            if st.button("Verify Vehicle"):
                if reg:
                    st.json({"registration": reg.upper(), "make": "Toyota", "model": "Corolla", "status": "Valid"})
        with c2:
            lic = st.text_input("License Number")
            if st.button("Verify License"):
                if lic:
                    st.json({"license": lic, "name": "John Doe", "class": "B", "status": "Valid"})

    # ---- AI DEMO ----
    elif page == "🤖 AI Demo":
        st.title("🤖 AI Demo")
        tab1, tab2 = st.tabs(["📸 Plate Detection", "💬 Chatbot"])
        with tab1:
            st.warning("Upload image for plate detection.")
            uploaded = st.file_uploader("Image", type=['jpg','png'])
            if uploaded:
                st.image(uploaded, width=200)
                st.success("✅ Plate: BD-123-ABC")
        with tab2:
            msg = st.text_input("Ask about traffic rules...")
            if msg:
                st.info("🤖 Speeding fines range from $50 to $500.")

    st.divider()
    st.caption("DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data")
