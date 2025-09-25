#!/usr/bin/env python3
"""
Script to create an admin user for the Harvester Tracking Platform
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.user import User
from app.utils.auth import get_password_hash

def create_admin_user():
    """Create an admin user if it doesn't exist"""
    db = SessionLocal()
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.email == "admin@harvester.com").first()
        if admin_user:
            print("Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@harvester.com",
            name="System Administrator",
            hashed_password=get_password_hash("admin123"),
            state="California",
            billing_method="per_acre",
            equipment_owned=True,
            equipment_details="System administrator account",
            is_active=True,
            is_admin=True
        )
        
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully!")
        print("Email: admin@harvester.com")
        print("Password: admin123")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
