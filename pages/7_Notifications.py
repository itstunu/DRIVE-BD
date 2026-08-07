import streamlit as st
import auth
from db import get_notifications, mark_notification_read
import pandas as pd

# ---- MUST BE FIRST STREAMLIT COMMAND ----
st.set_page_config(
    page_title="Notifications - DriveBD",
    page_icon="🔔",
    layout="wide"
)

# ---- Check Authentication ----
auth.require_login()

# ---- Page Content ----
st.title("🔔 Notifications")

user = auth.current_user()
user_id = user.get('user_id')

notifications = get_notifications(user_id)

if notifications:
    # Mark all as read button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("✅ Mark All Read"):
            for n in notifications:
                if not n.get('is_read', False):
                    mark_notification_read(n['id'])
            st.rerun()
    
    # Display notifications
    for n in notifications:
        with st.container():
            col1, col2 = st.columns([6, 1])
            with col1:
                if n.get('is_read', False):
                    st.markdown(f"**{n.get('title', 'Notification')}**")
                    st.caption(n.get('message', ''))
                else:
                    st.markdown(f"🔔 **{n.get('title', 'Notification')}**")
                    st.caption(n.get('message', ''))
            with col2:
                if not n.get('is_read', False):
                    if st.button("Mark Read", key=f"mark_{n['id']}"):
                        mark_notification_read(n['id'])
                        st.rerun()
            st.divider()
else:
    st.info("📭 No notifications")