import streamlit as st
import auth
from db import get_appeals, add_appeal_to_db, get_violations
import pandas as pd

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="Appeals - DriveBD",
    page_icon="⚖️",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()

# ---- Page Content ----
st.title("⚖️ Violation Appeals")

user = auth.current_user()
user_id = user.get('user_id')
role = user.get('role')

# ---- File Appeal ----
with st.expander("📝 File New Appeal", expanded=False):
    violations = get_violations()
    pending_violations = [v for v in violations if v.get('status') == 'pending']
    
    if pending_violations:
        with st.form("appeal_form"):
            violation_options = {v['id']: f"{v['vehicle_number']} - {v['violation_type']} (${v['fine_amount']})" 
                               for v in pending_violations}
            selected_violation = st.selectbox("Select Violation to Appeal", list(violation_options.keys()),
                                            format_func=lambda x: violation_options[x])
            
            reason = st.text_area("Appeal Reason *", placeholder="Explain why you're appealing this violation...")
            
            submitted = st.form_submit_button("Submit Appeal")
            
            if submitted and selected_violation and reason:
                appeal_data = {
                    'violation_id': selected_violation,
                    'user_id': user_id,
                    'reason': reason
                }
                result = add_appeal_to_db(appeal_data)
                if result:
                    st.success("✅ Appeal submitted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to submit appeal.")
    else:
        st.info("No pending violations to appeal.")

# ---- Display Appeals ----
st.subheader("📋 Your Appeals")

appeals = get_appeals(user_id)

if appeals:
    df = pd.DataFrame(appeals)
    st.dataframe(
        df[['submission_date', 'reason', 'status', 'decision', 'reviewer_comments']],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No appeals found.")