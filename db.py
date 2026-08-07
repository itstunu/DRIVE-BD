"""
DriveBD - Database Layer (Local SQLite)
"""
import os
import sqlite3
import streamlit as st
from datetime import datetime
import uuid

DB_PATH = "data/drivebd.db"

# ========== DATABASE INITIALIZATION ==========

def init_db():
    """Initialize the database with tables"""
    os.makedirs("data", exist_ok=True)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'driver',
                nid TEXT,
                phone TEXT,
                license_no TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Vehicles table
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
                status TEXT DEFAULT 'active',
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Violations table
        c.execute('''
            CREATE TABLE IF NOT EXISTS violations (
                id TEXT PRIMARY KEY,
                vehicle_number TEXT,
                violation_type TEXT NOT NULL,
                violation_date TEXT,
                location TEXT,
                fine_amount REAL,
                status TEXT DEFAULT 'pending',
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Payments table
        c.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id TEXT PRIMARY KEY,
                violation_id TEXT,
                user_id TEXT,
                amount REAL NOT NULL,
                payment_date TEXT,
                payment_method TEXT,
                status TEXT DEFAULT 'pending',
                transaction_id TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Documents table
        c.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                document_name TEXT NOT NULL,
                document_type TEXT NOT NULL,
                file_url TEXT,
                upload_date TEXT,
                expiry_date TEXT,
                verification_status TEXT DEFAULT 'pending',
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Notifications table
        c.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                is_read INTEGER DEFAULT 0,
                read_at TEXT,
                created_at TEXT
            )
        ''')
        
        # Appeals table
        c.execute('''
            CREATE TABLE IF NOT EXISTS appeals (
                id TEXT PRIMARY KEY,
                violation_id TEXT,
                user_id TEXT,
                reason TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                submission_date TEXT,
                review_date TEXT,
                decision TEXT,
                reviewer_comments TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Activity logs table
        c.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
        return True
        
    except Exception as e:
        print(f"⚠️ Database initialization error: {e}")
        return False

# ========== USER FUNCTIONS ==========

def get_user_by_email(email):
    """Get user by email"""
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
                'nid': row[5] if len(row) > 5 else '',
                'phone': row[6] if len(row) > 6 else '',
                'license_no': row[7] if len(row) > 7 else ''
            }
        return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def create_user_in_db(user_data):
    """Create a new user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        user_data['id'] = str(uuid.uuid4())
        user_data['created_at'] = datetime.now().isoformat()
        user_data['updated_at'] = datetime.now().isoformat()
        
        c.execute('''
            INSERT INTO users (id, name, email, password_hash, role, nid, phone, license_no, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data['id'],
            user_data['name'],
            user_data['email'],
            user_data['password_hash'],
            user_data['role'],
            user_data.get('nid', ''),
            user_data.get('phone', ''),
            user_data.get('license_no', ''),
            user_data['created_at'],
            user_data['updated_at']
        ))
        
        conn.commit()
        conn.close()
        return user_data
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def log_activity_db(user_id, action, details=None):
    """Log user activity"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        activity_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        c.execute('''
            INSERT INTO activity_logs (id, user_id, action, details, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (activity_id, user_id, action, details, timestamp))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error logging activity: {e}")
        return False

# ========== VEHICLE FUNCTIONS ==========

def get_vehicles(user_id=None):
    """Get vehicles"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if user_id:
            c.execute("SELECT * FROM vehicles WHERE user_id = ?", (user_id,))
        else:
            c.execute("SELECT * FROM vehicles")
        
        rows = c.fetchall()
        conn.close()
        
        vehicles = []
        for row in rows:
            vehicles.append({
                'id': row[0],
                'user_id': row[1],
                'registration_number': row[2],
                'make': row[3],
                'model': row[4],
                'year': row[5],
                'color': row[6],
                'chassis_number': row[7],
                'engine_number': row[8],
                'status': row[9]
            })
        return vehicles
    except Exception as e:
        print(f"Error getting vehicles: {e}")
        return []

def add_vehicle_to_db(vehicle_data):
    """Add a vehicle"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        vehicle_data['id'] = str(uuid.uuid4())
        vehicle_data['created_at'] = datetime.now().isoformat()
        vehicle_data['updated_at'] = datetime.now().isoformat()
        
        c.execute('''
            INSERT INTO vehicles (id, user_id, registration_number, make, model, year, color, chassis_number, engine_number, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vehicle_data['id'],
            vehicle_data.get('user_id'),
            vehicle_data['registration_number'],
            vehicle_data['make'],
            vehicle_data['model'],
            vehicle_data.get('year'),
            vehicle_data.get('color'),
            vehicle_data.get('chassis_number'),
            vehicle_data.get('engine_number'),
            vehicle_data.get('status', 'active'),
            vehicle_data['created_at'],
            vehicle_data['updated_at']
        ))
        
        conn.commit()
        conn.close()
        return vehicle_data
    except Exception as e:
        print(f"Error adding vehicle: {e}")
        return None

# ========== VIOLATION FUNCTIONS ==========

def get_violations(vehicle_number=None):
    """Get violations"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if vehicle_number:
            c.execute("SELECT * FROM violations WHERE vehicle_number = ?", (vehicle_number,))
        else:
            c.execute("SELECT * FROM violations")
        
        rows = c.fetchall()
        conn.close()
        
        violations = []
        for row in rows:
            violations.append({
                'id': row[0],
                'vehicle_number': row[1],
                'violation_type': row[2],
                'violation_date': row[3],
                'location': row[4],
                'fine_amount': row[5],
                'status': row[6]
            })
        return violations
    except Exception as e:
        print(f"Error getting violations: {e}")
        return []

def add_violation_to_db(violation_data):
    """Add a violation"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        violation_data['id'] = str(uuid.uuid4())
        violation_data['created_at'] = datetime.now().isoformat()
        violation_data['updated_at'] = datetime.now().isoformat()
        
        c.execute('''
            INSERT INTO violations (id, vehicle_number, violation_type, violation_date, location, fine_amount, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            violation_data['id'],
            violation_data['vehicle_number'],
            violation_data['violation_type'],
            violation_data.get('violation_date', datetime.now().isoformat()),
            violation_data.get('location', ''),
            violation_data.get('fine_amount', 0),
            violation_data.get('status', 'pending'),
            violation_data['created_at'],
            violation_data['updated_at']
        ))
        
        conn.commit()
        conn.close()
        return violation_data
    except Exception as e:
        print(f"Error adding violation: {e}")
        return None

def update_violation_status(violation_id, status):
    """Update violation status"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            UPDATE violations 
            SET status = ?, updated_at = ? 
            WHERE id = ?
        ''', (status, datetime.now().isoformat(), violation_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating violation: {e}")
        return False

# ========== PAYMENT FUNCTIONS ==========

def get_payments(user_id=None):
    """Get payments"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if user_id:
            c.execute("SELECT * FROM payments WHERE user_id = ?", (user_id,))
        else:
            c.execute("SELECT * FROM payments")
        
        rows = c.fetchall()
        conn.close()
        
        payments = []
        for row in rows:
            payments.append({
                'id': row[0],
                'violation_id': row[1],
                'user_id': row[2],
                'amount': row[3],
                'payment_date': row[4],
                'payment_method': row[5],
                'status': row[6],
                'transaction_id': row[7]
            })
        return payments
    except Exception as e:
        print(f"Error getting payments: {e}")
        return []

def add_payment_to_db(payment_data):
    """Add a payment"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        payment_data['id'] = str(uuid.uuid4())
        payment_data['payment_date'] = datetime.now().isoformat()
        payment_data['created_at'] = datetime.now().isoformat()
        payment_data['updated_at'] = datetime.now().isoformat()
        
        c.execute('''
            INSERT INTO payments (id, violation_id, user_id, amount, payment_date, payment_method, status, transaction_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            payment_data['id'],
            payment_data['violation_id'],
            payment_data['user_id'],
            payment_data['amount'],
            payment_data['payment_date'],
            payment_data.get('payment_method', 'cash'),
            payment_data.get('status', 'pending'),
            payment_data.get('transaction_id', ''),
            payment_data['created_at'],
            payment_data['updated_at']
        ))
        
        conn.commit()
        conn.close()
        return payment_data
    except Exception as e:
        print(f"Error adding payment: {e}")
        return None

# ========== DOCUMENT FUNCTIONS ==========

def get_documents(user_id=None):
    """Get documents"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if user_id:
            c.execute("SELECT * FROM documents WHERE user_id = ?", (user_id,))
        else:
            c.execute("SELECT * FROM documents")
        
        rows = c.fetchall()
        conn.close()
        
        documents = []
        for row in rows:
            documents.append({
                'id': row[0],
                'user_id': row[1],
                'document_name': row[2],
                'document_type': row[3],
                'file_url': row[4],
                'upload_date': row[5],
                'expiry_date': row[6],
                'verification_status': row[7]
            })
        return documents
    except Exception as e:
        print(f"Error getting documents: {e}")
        return []

def add_document_to_db(document_data):
    """Add a document"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        document_data['id'] = str(uuid.uuid4())
        document_data['upload_date'] = datetime.now().isoformat()
        document_data['created_at'] = datetime.now().isoformat()
        document_data['updated_at'] = datetime.now().isoformat()
        
        c.execute('''
            INSERT INTO documents (id, user_id, document_name, document_type, file_url, upload_date, expiry_date, verification_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            document_data['id'],
            document_data['user_id'],
            document_data['document_name'],
            document_data['document_type'],
            document_data.get('file_url', ''),
            document_data['upload_date'],
            document_data.get('expiry_date', ''),
            document_data.get('verification_status', 'pending'),
            document_data['created_at'],
            document_data['updated_at']
        ))
        
        conn.commit()
        conn.close()
        return document_data
    except Exception as e:
        print(f"Error adding document: {e}")
        return None

# ========== NOTIFICATION FUNCTIONS ==========

def get_notifications(user_id):
    """Get notifications"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        rows = c.fetchall()
        conn.close()
        
        notifications = []
        for row in rows:
            notifications.append({
                'id': row[0],
                'user_id': row[1],
                'title': row[2],
                'message': row[3],
                'type': row[4],
                'is_read': row[5] == 1,
                'read_at': row[6],
                'created_at': row[7]
            })
        return notifications
    except Exception as e:
        print(f"Error getting notifications: {e}")
        return []

def add_notification_to_db(notification_data):
    """Add a notification"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        notification_data['id'] = str(uuid.uuid4())
        notification_data['created_at'] = datetime.now().isoformat()
        notification_data['is_read'] = 0
        
        c.execute('''
            INSERT INTO notifications (id, user_id, title, message, type, is_read, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            notification_data['id'],
            notification_data['user_id'],
            notification_data['title'],
            notification_data['message'],
            notification_data.get('type', 'info'),
            notification_data['is_read'],
            notification_data['created_at']
        ))
        
        conn.commit()
        conn.close()
        return notification_data
    except Exception as e:
        print(f"Error adding notification: {e}")
        return None

def mark_notification_read(notification_id):
    """Mark notification as read"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            UPDATE notifications 
            SET is_read = 1, read_at = ? 
            WHERE id = ?
        ''', (datetime.now().isoformat(), notification_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error marking notification read: {e}")
        return False

# ========== APPEAL FUNCTIONS ==========

def get_appeals(user_id=None):
    """Get appeals"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if user_id:
            c.execute("SELECT * FROM appeals WHERE user_id = ?", (user_id,))
        else:
            c.execute("SELECT * FROM appeals")
        
        rows = c.fetchall()
        conn.close()
        
        appeals = []
        for row in rows:
            appeals.append({
                'id': row[0],
                'violation_id': row[1],
                'user_id': row[2],
                'reason': row[3],
                'status': row[4],
                'submission_date': row[5],
                'review_date': row[6],
                'decision': row[7],
                'reviewer_comments': row[8]
            })
        return appeals
    except Exception as e:
        print(f"Error getting appeals: {e}")
        return []

def add_appeal_to_db(appeal_data):
    """Add an appeal"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        appeal_data['id'] = str(uuid.uuid4())
        appeal_data['submission_date'] = datetime.now().isoformat()
        appeal_data['status'] = 'pending'
        appeal_data['created_at'] = datetime.now().isoformat()
        appeal_data['updated_at'] = datetime.now().isoformat()
        
        c.execute('''
            INSERT INTO appeals (id, violation_id, user_id, reason, status, submission_date, review_date, decision, reviewer_comments, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            appeal_data['id'],
            appeal_data['violation_id'],
            appeal_data['user_id'],
            appeal_data['reason'],
            appeal_data['status'],
            appeal_data['submission_date'],
            appeal_data.get('review_date', ''),
            appeal_data.get('decision', ''),
            appeal_data.get('reviewer_comments', ''),
            appeal_data['created_at'],
            appeal_data['updated_at']
        ))
        
        conn.commit()
        conn.close()
        return appeal_data
    except Exception as e:
        print(f"Error adding appeal: {e}")
        return None
