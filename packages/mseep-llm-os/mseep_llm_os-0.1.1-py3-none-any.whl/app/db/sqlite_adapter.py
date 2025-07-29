"""SQLite adapter for phi AssistantStorage"""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from phi.storage.assistant.base import AssistantStorage
from phi.assistant import AssistantRun
from phi.utils.dttm import current_datetime

from app.db.sqlite import SQLiteStorage

class SQLiteAssistantAdapter(AssistantStorage):
    """Adapter to use SQLiteStorage with phi AssistantStorage interface"""
    
    def __init__(self):
        """Initialize adapter with SQLiteStorage"""
        self.storage = SQLiteStorage()
    
    def create(self, messages: List[Dict[str, Any]], metadata: Dict[str, Any], 
               user_id: Optional[str] = None, assistant_name: str = "LYRAIOS") -> str:
        """Create a new run"""
        run_id = str(uuid.uuid4())
        
        # Create an AssistantRun object
        assistant_run = AssistantRun(
            run_id=run_id,
            user_id=user_id,
            name=assistant_name
        )
        
        # Set metadata fields
        if metadata:
            for key, value in metadata.items():
                if hasattr(assistant_run, key):
                    setattr(assistant_run, key, value)
                else:
                    # Store in assistant_data if not a direct attribute
                    if assistant_run.assistant_data is None:
                        assistant_run.assistant_data = {}
                    assistant_run.assistant_data[key] = value
        
        # Save to storage
        self.upsert(assistant_run, messages=messages)
        
        return run_id
    
    def get(self, run_id: str) -> Optional[AssistantRun]:
        """Get a run by ID"""
        return self.read(run_id)
    
    def update(self, run_id: str, messages: List[Dict[str, Any]], metadata: Dict[str, Any]) -> None:
        """Update a run"""
        # Get existing run
        assistant_run = self.read(run_id)
        if assistant_run:
            # Update metadata
            if metadata:
                for key, value in metadata.items():
                    if hasattr(assistant_run, key):
                        setattr(assistant_run, key, value)
                    else:
                        # Store in assistant_data if not a direct attribute
                        if assistant_run.assistant_data is None:
                            assistant_run.assistant_data = {}
                        assistant_run.assistant_data[key] = value
            
            # Update the run
            self.upsert(assistant_run, messages=messages)
    
    def get_all_run_ids(self, user_id: Optional[str] = None) -> List[str]:
        """Get all run IDs"""
        # SQLiteStorage does not support filtering by user ID, so we need to manually filter
        all_runs = self.storage.get_all_runs()
        if user_id:
            return [run["run_id"] for run in all_runs if run.get("user_id") == user_id]
        return self.storage.get_all_run_ids()
    
    def get_all_runs(self, user_id: Optional[str] = None) -> List[AssistantRun]:
        """Get all runs"""
        all_runs = self.storage.get_all_runs()
        runs = []
        for data in all_runs:
            if user_id is None or data.get("user_id") == user_id:
                assistant_run = self._create_assistant_run_from_data(data)
                if assistant_run:
                    runs.append(assistant_run)
        return runs
    
    def delete(self, run_id: str) -> None:
        """Delete a run"""
        self.storage.delete_run(run_id)
    
    def read(self, run_id: str) -> Optional[AssistantRun]:
        """Read a run by ID and return an AssistantRun object"""
        data = self.storage.get_run(run_id)
        if data:
            return self._create_assistant_run_from_data(data)
        return None
    
    def _create_assistant_run_from_data(self, data: Dict[str, Any]) -> Optional[AssistantRun]:
        """Helper method to create an AssistantRun from storage data"""
        try:
            # Extract basic fields
            run_id = data.get("run_id")
            user_id = data.get("user_id")
            assistant_name = data.get("assistant_name", "LYRAIOS")
            
            # Create the AssistantRun object
            assistant_run = AssistantRun(
                run_id=run_id,
                user_id=user_id,
                name=assistant_name
            )
            
            # Set created_at and updated_at if available
            if "created_at" in data:
                if isinstance(data["created_at"], str):
                    assistant_run.created_at = datetime.fromisoformat(data["created_at"])
                else:
                    assistant_run.created_at = data["created_at"]
            
            # Extract metadata
            metadata = data.get("metadata", {})
            if isinstance(metadata, dict):
                # Set standard fields from metadata
                if "assistant_data" in metadata:
                    assistant_run.assistant_data = metadata["assistant_data"]
                if "run_data" in metadata:
                    assistant_run.run_data = metadata["run_data"]
                if "user_data" in metadata:
                    assistant_run.user_data = metadata["user_data"]
                if "task_data" in metadata:
                    assistant_run.task_data = metadata["task_data"]
                if "llm" in metadata:
                    assistant_run.llm = metadata["llm"]
                if "memory" in metadata:
                    assistant_run.memory = metadata["memory"]
                
                # Set any other fields
                for key, value in metadata.items():
                    if not hasattr(assistant_run, key):
                        setattr(assistant_run, key, value)
            
            return assistant_run
        except Exception as e:
            print(f"Error creating AssistantRun from data: {e}")
            return None
    
    def upsert(self, row: AssistantRun, **kwargs) -> AssistantRun:
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
            self.storage.save_run(
                run_id=run_id,
                messages=messages,
                metadata=metadata,
                user_id=row.user_id,
                assistant_name=row.name
            )

            # Return the updated AssistantRun object
            return row
        except Exception as e:
            raise RuntimeError(f"[storage] Could not upsert run: {str(e)}")