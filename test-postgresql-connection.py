#!/usr/bin/env python3
"""
PostgreSQL Connection Test Script for Harvester Tracking Platform
This script tests the PostgreSQL database connection and verifies the setup.
"""

import os
import sys
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def test_postgresql_connection():
    """Test PostgreSQL connection and database setup."""
    print("🐘 Testing PostgreSQL Connection for Harvester Tracking Platform")
    print("=" * 60)
    
    # Get database URL from environment or use default
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/harvester_tracking")
    
    print(f"📊 Database URL: {database_url}")
    print()
    
    try:
        # Test SQLAlchemy connection
        print("🔌 Testing SQLAlchemy connection...")
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ PostgreSQL version: {version}")
            
            # Test database exists
            result = connection.execute(text("SELECT current_database();"))
            db_name = result.fetchone()[0]
            print(f"✅ Connected to database: {db_name}")
            
            # Check if tables exist
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE';
            """))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"✅ Found {len(tables)} tables: {', '.join(tables)}")
            else:
                print("⚠️  No tables found - run migrations first")
            
            print()
            print("🎉 PostgreSQL connection test successful!")
            return True
            
    except SQLAlchemyError as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_psycopg2_connection():
    """Test direct psycopg2 connection."""
    print("🔌 Testing direct psycopg2 connection...")
    
    try:
        # Parse database URL
        url_parts = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/harvester_tracking")
        if url_parts.startswith("postgresql://"):
            url_parts = url_parts[12:]  # Remove postgresql://
        
        user_pass, host_port_db = url_parts.split("@")
        user, password = user_pass.split(":")
        host_port, database = host_port_db.split("/")
        host, port = host_port.split(":")
        
        conn = psycopg2.connect(
            host=host,
            port=int(port),
            database=database,
            user=user,
            password=password
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Direct psycopg2 connection successful: {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Direct psycopg2 connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting PostgreSQL connection tests...")
    print()
    
    # Test both connection methods
    sqlalchemy_ok = test_postgresql_connection()
    print()
    psycopg2_ok = test_psycopg2_connection()
    
    print()
    print("=" * 60)
    if sqlalchemy_ok and psycopg2_ok:
        print("🎉 All PostgreSQL connection tests passed!")
        print("✅ Your PostgreSQL setup is working correctly")
        sys.exit(0)
    else:
        print("❌ Some PostgreSQL connection tests failed")
        print("💡 Check your PostgreSQL installation and configuration")
        sys.exit(1)
