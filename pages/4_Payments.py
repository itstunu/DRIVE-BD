import streamlit as st
import auth
from db import get_payments, add_payment_to_db, get_violations
import pandas as pd

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="Payments - DriveBD",
    page_icon="💰",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()

# ---- Page Content ----
st.title("💰 Payment Management")

user = auth.current_user()
user_id = user.get('user_id')
role = user.get('role')

# ---- Process Payment ----
with st.expander("💳 Make Payment", expanded=False):
    violations = get_violations()
    pending_violations = [v for v in violations if v.get('status') == 'pending']
    
    if pending_violations:
        with st.form("payment_form"):
            violation_options = {v['id']: f"{v['vehicle_number']} - {v['violation_type']} (${v['fine_amount']})" 
                               for v in pending_violations}
            selected_violation = st.selectbox("Select Violation to Pay", list(violation_options.keys()),
                                            format_func=lambda x: violation_options[x])
            
            payment_method = st.selectbox("Payment Method", ["cash", "card", "mobile_banking"])
            
            submitted = st.form_submit_button("💳 Pay Now")
            
            if submitted and selected_violation:
                violation = next(v for v in pending_violations if v['id'] == selected_violation)
                payment_data = {
                    'violation_id': selected_violation,
                    'user_id': user_id,
                    'amount': violation['fine_amount'],
                    'payment_method': payment_method,
                    'status': 'completed',
                    'transaction_id': f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                }
                result = add_payment_to_db(payment_data)
                if result:
                    st.success(f"✅ Payment of ${violation['fine_amount']} completed!")
                    st.rerun()
                else:
                    st.error("❌ Payment failed. Please try again.")
    else:
        st.info("No pending violations to pay.")

# ---- Payment History ----
st.subheader("📋 Payment History")

payments = get_payments(user_id)

if payments:
    df = pd.DataFrame(payments)
    st.dataframe(
        df[['amount', 'payment_date', 'payment_method', 'status', 'transaction_id']],
        use_container_width=True,
        hide_index=True
    )
    
    total = sum([p.get('amount', 0) for p in payments if p.get('status') == 'completed'])
    st.metric("💰 Total Paid", f"${total:,.2f}")
else:
    st.info("No payment history found.")