"""Test script for SQLite adapter"""

import logging
import sys
import os

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.db.sqlite_adapter import SQLiteAssistantAdapter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_sqlite_adapter():
    """Test SQLite adapter"""
    try:
        adapter = SQLiteAssistantAdapter()
        
        # Test creation
        run_id = adapter.create(
            messages=[{"role": "user", "content": "Hello"}],
            metadata={},
            user_id="test_user",
            assistant_name="LYRAIOS"
        )
        logger.info(f"Created run with ID: {run_id}")
        
        # Test retrieval
        run = adapter.get(run_id)
        logger.info(f"Retrieved run: {run}")
        
        # Test update
        adapter.update(
            run_id=run_id,
            messages=[
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ],
            metadata={"updated": True}
        )
        logger.info("Updated run")
        
        # Test retrieval of all IDs
        run_ids = adapter.get_all_run_ids()
        logger.info(f"All run IDs: {run_ids}")
        
        # Test retrieval of all runs
        runs = adapter.get_all_runs()
        logger.info(f"All runs: {len(runs)}")
        
        # Test read and upsert methods
        data = adapter.read(run_id)
        logger.info(f"Read run: {data}")
        
        new_run_id = "test_run_id"
        adapter.upsert(
            run_id=new_run_id,
            data={
                "run_id": new_run_id,
                "messages": [{"role": "user", "content": "Test"}],
                "metadata": {},
                "user_id": "test_user",
                "assistant_name": "LYRAIOS"
            }
        )
        logger.info("Upserted run")
        
        # Test deletion
        adapter.delete(run_id)
        logger.info("Deleted run")
        adapter.delete(new_run_id)
        logger.info("Deleted test run")
        
        return True
    except Exception as e:
        logger.error(f"SQLite adapter test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_sqlite_adapter()
    if success:
        logger.info("SQLite adapter test passed!")
    else:
        logger.error("SQLite adapter test failed!") 