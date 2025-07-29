from typing import Optional, List, Dict, Any
import uuid
from phi.storage.assistant.base import AssistantStorage
from phi.assistant.run import AssistantRun
import logging

logger = logging.getLogger(__name__)

class AssistantStorageAdapter(AssistantStorage):
    def __init__(self):
        try:
            from app.db.factory import get_storage
            self._storage = get_storage()
            # Verify if storage is available
            self._storage.get_all_run_ids()
        except Exception as e:
            logger.error(f"Failed to initialize storage adapter: {e}")
            raise RuntimeError("[storage] Could not initialize storage adapter")

    def create(self, messages: List[Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None, **kwargs) -> str:
        """Create a new run"""
        try:
            run_id = str(uuid.uuid4())
            self._storage.save_run(
                run_id=run_id,
                messages=messages or [],
                metadata=metadata or {},
                user_id=kwargs.get("user_id"),
                assistant_name=kwargs.get("assistant_name")
            )
            logger.debug(f"Created new run with ID: {run_id}")
            return run_id
        except Exception as e:
            logger.error(f"Failed to create run: {e}")
            raise RuntimeError(f"[storage] Could not create run: {str(e)}")

    def read(self, run_id: str) -> Optional[AssistantRun]:
        """Read a run by ID and return as AssistantRun object"""
        try:
            result = self._storage.get_run(run_id)
            if result:
                # Extract metadata from stored data
                metadata = result.get("metadata", {})
                
                # Create AssistantRun object
                return AssistantRun(
                    run_id=result["run_id"],
                    name=result.get("assistant_name"),
                    user_id=result.get("user_id"),
                    messages=result.get("messages", []),
                    assistant_data=metadata.get("assistant_data"),
                    run_data=metadata.get("run_data"),
                    user_data=metadata.get("user_data"),
                    task_data=metadata.get("task_data")
                )
            return None
        except Exception as e:
            logger.error(f"Failed to read run: {e}")
            return None

    def upsert(
        self,
        row: AssistantRun,
        **kwargs
    ) -> AssistantRun:
        """Update or insert a run using an AssistantRun object and return the updated run."""
        try:
            # Ensure the input is an AssistantRun object
            if not isinstance(row, AssistantRun):
                raise TypeError("Expected an AssistantRun object for the 'row' parameter.")

            # Extract properties from AssistantRun object
            run_id = row.run_id
            
            # Get messages from kwargs, as AssistantRun does not store messages
            messages = kwargs.get("messages", [])
            
            # Build metadata dictionary
            metadata = {
                "assistant_data": row.assistant_data,
                "run_data": row.run_data,
                "user_data": row.user_data,
                "task_data": row.task_data,
                "llm": row.llm,
                "memory": row.memory,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None
            }

            # Ensure required parameters exist
            if not run_id:
                raise ValueError("run_id is required")

            # Call underlying storage method
            self._storage.save_run(
                run_id=run_id,
                messages=messages,
                metadata=metadata,
                user_id=row.user_id,
                assistant_name=row.name
            )
            logger.debug(f"Upserted run with ID: {run_id}")

            # Return the updated AssistantRun object
            return row
        except Exception as e:
            logger.error(f"Failed to upsert run: {e}")
            raise RuntimeError(f"[storage] Could not upsert run: {str(e)}")

    def delete(self, run_id: str) -> None:
        """Delete a run"""
        try:
            if not run_id:
                raise ValueError("run_id is required")
            
            self._storage.delete_run(run_id)
            logger.debug(f"Deleted run with ID: {run_id}")
        except Exception as e:
            logger.error(f"Failed to delete run: {e}")
            raise RuntimeError(f"[storage] Could not delete run: {str(e)}")

    def get_all_run_ids(
        self,
        user_id: Optional[str] = None,
        assistant_name: Optional[str] = None,
    ) -> List[str]:
        """Get all run IDs"""
        try:
            return self._storage.get_all_run_ids()
        except Exception as e:
            logger.error(f"Failed to get run IDs: {e}")
            return []

    def get_all_runs(
        self,
        user_id: Optional[str] = None,
        assistant_name: Optional[str] = None,
    ) -> List[AssistantRun]:
        """Get all runs as AssistantRun objects"""
        try:
            runs = self._storage.get_all_runs()
            return [
                AssistantRun(
                    run_id=run["run_id"],
                    name=run.get("assistant_name"),
                    user_id=run.get("user_id"),
                    messages=run.get("messages", []),
                    assistant_data=run.get("metadata", {}).get("assistant_data"),
                    run_data=run.get("metadata", {}).get("run_data"),
                    user_data=run.get("metadata", {}).get("user_data"),
                    task_data=run.get("metadata", {}).get("task_data")
                )
                for run in runs
            ]
        except Exception as e:
            logger.error(f"Failed to get all runs: {e}")
            return []

# Export class name
__all__ = ['AssistantStorageAdapter'] 