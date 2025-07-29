import logging
import os
from typing import Optional
import sqlite3
import psycopg
from pathlib import Path
from .config import db_settings

logger = logging.getLogger(__name__)

def init_sqlite_db(db_path: str) -> bool:
    """Initialize SQLite database and tables"""
    try:
        # Ensure data directory exists and has correct permissions
        db_dir = os.path.dirname(db_path)
        os.makedirs(db_dir, exist_ok=True)
        
        logger.info(f"Initializing SQLite database at {db_path}")
        
        # Test file write permission
        if os.path.exists(db_path):
            if not os.access(db_path, os.W_OK):
                logger.error(f"No write permission for database file: {db_path}")
                return False
        else:
            # Test directory write permission
            if not os.access(db_dir, os.W_OK):
                logger.error(f"No write permission for directory: {db_dir}")
                return False
        
        with sqlite3.connect(db_path) as conn:
            # Assistant runs table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS assistant_runs (
                    run_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    assistant_name TEXT,
                    created_at TIMESTAMP,
                    messages TEXT,
                    metadata TEXT
                )
            """)
            conn.commit()
            
        logger.info("SQLite database initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize SQLite database: {str(e)}")
        return False

def init_postgres_db(db_url: str):
    """Initialize PostgreSQL database and tables"""
    logger.info("Initializing PostgreSQL database")
    
    # First try to create database if it doesn't exist
    db_name = db_settings.POSTGRES_DB
    base_url = db_url.rsplit('/', 1)[0]
    
    try:
        with psycopg.connect(f"{base_url}/postgres") as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                # Check if database exists
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
                if not cur.fetchone():
                    cur.execute(f"CREATE DATABASE {db_name}")
                    logger.info(f"Created database {db_name}")
    except Exception as e:
        logger.warning(f"Could not create database: {e}")
    
    # Now create tables
    try:
        with psycopg.connect(db_url) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                # Assistant runs table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS assistant_runs (
                        run_id TEXT PRIMARY KEY,
                        user_id TEXT,
                        assistant_name TEXT,
                        created_at TIMESTAMP,
                        messages JSONB,
                        metadata JSONB
                    )
                """)
                
                # Vector storage table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS vectors (
                        id TEXT PRIMARY KEY,
                        collection TEXT,
                        embedding vector(1536),
                        metadata JSONB
                    )
                """)
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

def init_database() -> bool:
    """Initialize database based on configuration"""
    if db_settings.AUTO_CREATE_DB:
        try:
            if db_settings.is_sqlite:
                return init_sqlite_db(db_settings.absolute_db_path)
            elif db_settings.is_postgres:
                return init_postgres_db(db_settings.db_url)
            else:
                logger.error(f"Unsupported database type: {db_settings.DATABASE_TYPE}")
                return False
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            return False
    return True 