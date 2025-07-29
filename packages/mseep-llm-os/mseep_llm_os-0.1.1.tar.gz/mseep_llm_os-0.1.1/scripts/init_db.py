#!/usr/bin/env python
import os
import logging
from pathlib import Path
from db.init import init_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Initialize database"""
    try:
        # Ensure data directory exists
        data_dir = Path.cwd() / "data"
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize database
        init_database()
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    main() 