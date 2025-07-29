#!/usr/bin/env python
import os
import logging
from pathlib import Path
from db.factory import get_storage
from db.config import db_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database():
    """Check database status"""
    try:
        logger.info(f"Checking database configuration...")
        logger.info(f"Database type: {db_settings.DATABASE_TYPE}")
        
        if db_settings.is_sqlite:
            db_path = db_settings.absolute_db_path
            logger.info(f"Database path: {db_path}")
            
            # Check directory permissions
            db_dir = os.path.dirname(db_path)
            if not os.path.exists(db_dir):
                logger.warning(f"Database directory does not exist: {db_dir}")
            elif not os.access(db_dir, os.W_OK):
                logger.error(f"No write permission for directory: {db_dir}")
                return False
                
            # Check file permissions
            if os.path.exists(db_path):
                if not os.access(db_path, os.W_OK):
                    logger.error(f"No write permission for database file: {db_path}")
                    return False
        
        # Test storage connection
        storage = get_storage()
        storage.get_all_run_ids()
        
        logger.info("Database check completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database check failed: {e}")
        return False

if __name__ == "__main__":
    if check_database():
        print("Database is ready to use")
    else:
        print("Database check failed. Please check the logs for details.") 