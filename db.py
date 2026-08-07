"""
DriveBD - Database Layer with Supabase
"""
import os
import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import uuid

# Initialize Supabase client
@st.cache_resource
def get_supabase():
    """Get Supabase client (cached for performance)"""
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            # Fallback to local SQLite if no Supabase credentials
            print("⚠️ Supabase credentials not found. Using local SQLite...")
            return None
        
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"⚠️ Supabase connection failed: {e}. Using local SQLite...")
        return None

# Database path for local SQLite (fallback)
DB_PATH = "data/drivebd.db"

# ========== USER FUNCTIONS ==========

def get_user_by_email(email):
    """Get user by email from Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            result = supabase.table('users').select('*').eq('email', email).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    # Fallback to local SQLite
    return get_user_by_email_local(email)

def create_user_in_db(user_data):
    """Create a new user in Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            # Add timestamps
            user_data['id'] = str(uuid.uuid4())
            user_data['created_at'] = datetime.now().isoformat()
            user_data['updated_at'] = datetime.now().isoformat()
            
            result = supabase.table('users').insert(user_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    # Fallback to local SQLite
    return create_user_local(user_data)

def update_user_email(user_id, new_email):
    """Update user email in Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            result = supabase.table('users').update({
                'email': new_email,
                'updated_at': datetime.now().isoformat()
            }).eq('id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    return None

# ========== VEHICLE FUNCTIONS ==========

def get_vehicles(user_id=None):
    """Get vehicles from Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            query = supabase.table('vehicles').select('*')
            if user_id:
                query = query.eq('user_id', user_id)
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Supabase error: {e}")
            return []
    return []

def add_vehicle_to_db(vehicle_data):
    """Add a vehicle to Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            vehicle_data['id'] = str(uuid.uuid4())
            vehicle_data['created_at'] = datetime.now().isoformat()
            vehicle_data['updated_at'] = datetime.now().isoformat()
            
            result = supabase.table('vehicles').insert(vehicle_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    return None

def update_vehicle(vehicle_id, vehicle_data):
    """Update a vehicle in Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            vehicle_data['updated_at'] = datetime.now().isoformat()
            result = supabase.table('vehicles').update(vehicle_data).eq('id', vehicle_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    return None

def delete_vehicle(vehicle_id):
    """Delete a vehicle from Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            result = supabase.table('vehicles').delete().eq('id', vehicle_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    return None

# ========== VIOLATION FUNCTIONS ==========

def get_violations(vehicle_number=None):
    """Get violations from Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            query = supabase.table('violations').select('*')
            if vehicle_number:
                query = query.eq('vehicle_number', vehicle_number)
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Supabase error: {e}")
            return []
    return []

def add_violation_to_db(violation_data):
    """Add a violation to Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            violation_data['id'] = str(uuid.uuid4())
            violation_data['created_at'] = datetime.now().isoformat()
            
            result = supabase.table('violations').insert(violation_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    return None

def update_violation_status(violation_id, status):
    """Update violation status in Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            result = supabase.table('violations').update({
                'status': status,
                'updated_at': datetime.now().isoformat()
            }).eq('id', violation_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    return None

# ========== PAYMENT FUNCTIONS ==========

def get_payments(user_id=None):
    """Get payments from Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            query = supabase.table('payments').select('*')
            if user_id:
                query = query.eq('user_id', user_id)
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Supabase error: {e}")
            return []
    return []

def add_payment_to_db(payment_data):
    """Add a payment to Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            payment_data['id'] = str(uuid.uuid4())
            payment_data['payment_date'] = datetime.now().isoformat()
            
            result = supabase.table('payments').insert(payment_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    return None

# ========== DOCUMENT FUNCTIONS ==========

def get_documents(user_id=None):
    """Get documents from Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            query = supabase.table('documents').select('*')
            if user_id:
                query = query.eq('user_id', user_id)
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Supabase error: {e}")
            return []
    return []

def add_document_to_db(document_data):
    """Add a document to Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            document_data['id'] = str(uuid.uuid4())
            document_data['upload_date'] = datetime.now().isoformat()
            
            result = supabase.table('documents').insert(document_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    return None

# ========== NOTIFICATION FUNCTIONS ==========

def get_notifications(user_id):
    """Get notifications from Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            result = supabase.table('notifications').select('*').eq('user_id', user_id).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Supabase error: {e}")
            return []
    return []

def add_notification_to_db(notification_data):
    """Add a notification to Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            notification_data['id'] = str(uuid.uuid4())
            notification_data['created_at'] = datetime.now().isoformat()
            notification_data['is_read'] = False
            
            result = supabase.table('notifications').insert(notification_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    return None

def mark_notification_read(notification_id):
    """Mark notification as read in Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            result = supabase.table('notifications').update({
                'is_read': True,
                'read_at': datetime.now().isoformat()
            }).eq('id', notification_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    return None

# ========== APPEAL FUNCTIONS ==========

def get_appeals(user_id=None):
    """Get appeals from Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            query = supabase.table('appeals').select('*')
            if user_id:
                query = query.eq('user_id', user_id)
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Supabase error: {e}")
            return []
    return []

def add_appeal_to_db(appeal_data):
    """Add an appeal to Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            appeal_data['id'] = str(uuid.uuid4())
            appeal_data['submission_date'] = datetime.now().isoformat()
            appeal_data['status'] = 'pending'
            
            result = supabase.table('appeals').insert(appeal_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    return None

# ========== ACTIVITY LOG FUNCTIONS ==========

def log_activity_db(user_id, action, details=None):
    """Log user activity to Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            activity_data = {
                'id': str(uuid.uuid4()),
                'user_id': user_id,
                'action': action,
                'details': details,
                'timestamp': datetime.now().isoformat()
            }
            result = supabase.table('activity_logs').insert(activity_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Supabase error: {e}")
            return None
    return None

def get_activity_logs(user_id=None, limit=50):
    """Get activity logs from Supabase"""
    supabase = get_supabase()
    if supabase:
        try:
            query = supabase.table('activity_logs').select('*').order('timestamp', desc=True).limit(limit)
            if user_id:
                query = query.eq('user_id', user_id)
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Supabase error: {e}")
            return []
    return []

# ========== LOCAL SQLITE FALLBACK FUNCTIONS ==========

def get_user_by_email_local(email):
    """Local SQLite fallback for user lookup"""
    import sqlite3
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = c.fetchone()
        conn.close()
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'password_hash': row[3],
                'role': row[4],
                'nid': row[5],
                'phone': row[6],
                'license_no': row[7]
            }
        return None
    except Exception as e:
        print(f"Local DB error: {e}")
        return None

def create_user_local(user_data):
    """Local SQLite fallback for user creation"""
    import sqlite3
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (id, name, email, password_hash, role, nid, phone, license_no)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_data.get('id'),
            user_data.get('name'),
            user_data.get('email'),
            user_data.get('password_hash'),
            user_data.get('role'),
            user_data.get('nid'),
            user_data.get('phone'),
            user_data.get('license_no')
        ))
        conn.commit()
        conn.close()
        return user_data
    except Exception as e:
        print(f"Local DB error: {e}")
        return None

# ========== INITIALIZATION ==========

def init_db():
    """Initialize the database (create tables if needed)"""
    # For Supabase, tables are created manually in the dashboard
    # This function exists for backward compatibility
    
    # Check if Supabase is configured
    supabase = get_supabase()
    if supabase:
        print("✅ Using Supabase database")
        
        # Test connection
        try:
            test = supabase.table('users').select('count').limit(1).execute()
            print("✅ Supabase connection successful")
        except Exception as e:
            print(f"⚠️ Supabase connection test failed: {e}")
        
        return
    
    # If no Supabase, initialize local SQLite
    import sqlite3
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Create tables for local fallback
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'driver',
                nid TEXT,
                phone TEXT,
                license_no TEXT
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                registration_number TEXT UNIQUE NOT NULL,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER,
                color TEXT,
                chassis_number TEXT,
                engine_number TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Add more tables as needed...
        
        conn.commit()
        conn.close()
        print("✅ Local database initialized")
    except Exception as e:
        print(f"⚠️ Database initialization error: {e}")
