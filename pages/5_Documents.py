import streamlit as st
import auth
from db import get_documents, add_document_to_db
import pandas as pd
from datetime import datetime

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="Documents - DriveBD",
    page_icon="📄",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()

# ---- Page Content ----
st.title("📄 Document Management")

user = auth.current_user()
user_id = user.get('user_id')

# ---- Upload Document ----
with st.expander("📤 Upload Document", expanded=False):
    with st.form("upload_document_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            doc_name = st.text_input("Document Name *")
            doc_type = st.selectbox("Document Type *", [
                "Registration Certificate",
                "Insurance",
                "Tax Token",
                "Pollution Certificate",
                "Fitness Certificate",
                "Other"
            ])
        
        with col2:
            expiry_date = st.date_input("Expiry Date (if applicable)")
            uploaded_file = st.file_uploader("Choose file", type=['pdf', 'jpg', 'png', 'jpeg'])
        
        submitted = st.form_submit_button("Upload Document")
        
        if submitted and doc_name and uploaded_file:
            # In production, you'd save the file to cloud storage
            document_data = {
                'user_id': user_id,
                'document_name': doc_name,
                'document_type': doc_type,
                'file_url': uploaded_file.name,
                'expiry_date': expiry_date.isoformat() if expiry_date else '',
                'verification_status': 'pending'
            }
            result = add_document_to_db(document_data)
            if result:
                st.success("✅ Document uploaded successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to upload document.")

# ---- Display Documents ----
st.subheader("📋 Your Documents")

documents = get_documents(user_id)

if documents:
    df = pd.DataFrame(documents)
    st.dataframe(
        df[['document_name', 'document_type', 'upload_date', 'expiry_date', 'verification_status']],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No documents uploaded yet.")