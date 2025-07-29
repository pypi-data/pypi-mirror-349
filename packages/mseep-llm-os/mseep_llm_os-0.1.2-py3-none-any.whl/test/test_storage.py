"""Test script for storage implementation"""

import logging
from app.db.memory_storage import MemoryAssistantStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_storage():
    """Test storage implementation"""
    try:
        storage = MemoryAssistantStorage()
        
        # Test creation
        run_id = storage.create(
            messages=[{"role": "user", "content": "Hello"}],
            metadata={},
            user_id="test_user",
            assistant_name="LYRAIOS"
        )
        logger.info(f"Created run with ID: {run_id}")
        
        # Test retrieval
        run = storage.get(run_id)
        logger.info(f"Retrieved run: {run}")
        
        # Test update
        storage.update(
            run_id=run_id,
            messages=[
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ],
            metadata={"updated": True}
        )
        logger.info("Updated run")
        
        # Test retrieval of all IDs
        run_ids = storage.get_all_run_ids()
        logger.info(f"All run IDs: {run_ids}")
        
        # Test retrieval of all runs
        runs = storage.get_all_runs()
        logger.info(f"All runs: {len(runs)}")
        
        # Test deletion
        storage.delete(run_id)
        logger.info("Deleted run")
        
        # Test read and upsert methods
        new_run_id = "test_run_id"
        storage.upsert(
            run_id=new_run_id,
            data={
                "run_id": new_run_id,
                "messages": [{"role": "user", "content": "Test"}],
                "metadata": {},
                "user_id": "test_user",
                "assistant_name": "LYRAIOS",
                "created_at": "2023-01-01T00:00:00"
            }
        )
        logger.info("Upserted run")
        
        data = storage.read(new_run_id)
        logger.info(f"Read run: {data}")
        
        return True
    except Exception as e:
        logger.error(f"Storage test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_storage()
    if success:
        logger.info("Storage test passed!")
    else:
        logger.error("Storage test failed!") 