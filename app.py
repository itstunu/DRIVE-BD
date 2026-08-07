"""
DriveBD - Database Layer with Supabase Integration
"""
import os
from supabase import create_client, Client
from datetime import datetime
import streamlit as st

# Initialize Supabase client
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ Supabase credentials not found! Please add SUPABASE_URL and SUPABASE_KEY to secrets.")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def init_db():
    """Initialize database - creates tables if they don't exist"""
    # Tables should be created manually in Supabase SQL editor
    # This function just checks if connection works
    try:
        supabase.table('users').select('count').limit(1).execute()
        print("✅ Supabase connection successful")
    except Exception as e:
        print(f"⚠️ Error connecting to Supabase: {e}")

def get_user_by_email(email):
    """Get user by email"""
    try:
        result = supabase.table('users').select('*').eq('email', email.lower().strip()).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

def create_user(user_data):
    """Create a new user"""
    try:
        user_data['email'] = user_data['email'].lower().strip()
        user_data['created_at'] = datetime.now().isoformat()
        user_data['updated_at'] = datetime.now().isoformat()
        result = supabase.table('users').insert(user_data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def get_vehicles(user_id=None, registration_number=None):
    """Get vehicles (optionally filtered by user or registration number)"""
    try:
        query = supabase.table('vehicles').select('*')
        if user_id:
            query = query.eq('user_id', user_id)
        if registration_number:
            query = query.eq('registration_number', registration_number.upper())
        result = query.execute()
        return result.data
    except Exception as e:
        print(f"Error fetching vehicles: {e}")
        return []

def add_vehicle(vehicle_data):
    """Add a new vehicle"""
    try:
        vehicle_data['created_at'] = datetime.now().isoformat()
        vehicle_data['updated_at'] = datetime.now().isoformat()
        result = supabase.table('vehicles').insert(vehicle_data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error adding vehicle: {e}")
        return None

def update_vehicle(registration_number, vehicle_data):
    """Update a vehicle"""
    try:
        vehicle_data['updated_at'] = datetime.now().isoformat()
        result = supabase.table('vehicles').update(vehicle_data).eq('registration_number', registration_number.upper()).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error updating vehicle: {e}")
        return None

def delete_vehicle(registration_number):
    """Delete a vehicle"""
    try:
        result = supabase.table('vehicles').delete().eq('registration_number', registration_number.upper()).execute()
        return len(result.data) > 0
    except Exception as e:
        print(f"Error deleting vehicle: {e}")
        return False

def get_violations(vehicle_number=None, user_id=None, status=None):
    """Get violations with optional filters"""
    try:
        query = supabase.table('violations').select('*')
        if vehicle_number:
            query = query.eq('vehicle_number', vehicle_number.upper())
        if user_id:
            query = query.eq('user_id', user_id)
        if status:
            query = query.eq('status', status)
        result = query.execute()
        return result.data
    except Exception as e:
        print(f"Error fetching violations: {e}")
        return []

def add_violation(violation_data):
    """Add a new violation"""
    try:
        violation_data['created_at'] = datetime.now().isoformat()
        violation_data['updated_at'] = datetime.now().isoformat()
        result = supabase.table('violations').insert(violation_data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error adding violation: {e}")
        return None

def update_violation(violation_id, violation_data):
    """Update a violation"""
    try:
        violation_data['updated_at'] = datetime.now().isoformat()
        result = supabase.table('violations').update(violation_data).eq('id', violation_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error updating violation: {e}")
        return None

def get_payments(violation_id=None, user_id=None, status=None):
    """Get payments with optional filters"""
    try:
        query = supabase.table('payments').select('*')
        if violation_id:
            query = query.eq('violation_id', violation_id)
        if user_id:
            query = query.eq('user_id', user_id)
        if status:
            query = query.eq('status', status)
        result = query.execute()
        return result.data
    except Exception as e:
        print(f"Error fetching payments: {e}")
        return []

def add_payment(payment_data):
    """Add a new payment"""
    try:
        payment_data['payment_date'] = datetime.now().isoformat()
        payment_data['created_at'] = datetime.now().isoformat()
        result = supabase.table('payments').insert(payment_data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error adding payment: {e}")
        return None

# Add more functions for: documents, appeals, notifications, service_history
