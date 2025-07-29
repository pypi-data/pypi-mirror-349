"""Memory-based storage implementation for LYRAIOS application"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import uuid
from phi.storage.assistant.base import AssistantStorage
from phi.assistant import AssistantRun

class MemoryAssistantStorage(AssistantStorage):
    """In-memory implementation of AssistantStorage"""
    
    def __init__(self):
        """Initialize storage"""
        self.runs = {}  # In-memory storage
    
    def create(self, messages: List[Dict[str, Any]], metadata: Dict[str, Any], 
               user_id: Optional[str] = None, assistant_name: str = "LYRAIOS") -> str:
        """Create a new run"""
        run_id = str(uuid.uuid4())
        self.runs[run_id] = {
            "run_id": run_id,
            "messages": messages,
            "metadata": metadata,
            "user_id": user_id,
            "assistant_name": assistant_name,
            "created_at": datetime.now().isoformat()
        }
        return run_id
    
    def get(self, run_id: str) -> Optional[AssistantRun]:
        """Get a run by ID"""
        if run_id in self.runs:
            data = self.runs[run_id]
            return AssistantRun(
                run_id=run_id,
                messages=data["messages"],
                metadata=data["metadata"],
                user_id=data["user_id"],
                assistant_name=data["assistant_name"]
            )
        return None
    
    def update(self, run_id: str, messages: List[Dict[str, Any]], metadata: Dict[str, Any]) -> None:
        """Update a run"""
        if run_id in self.runs:
            self.runs[run_id]["messages"] = messages
            self.runs[run_id]["metadata"] = metadata
    
    def get_all_run_ids(self, user_id: Optional[str] = None) -> List[str]:
        """Get all run IDs"""
        if user_id:
            return [run_id for run_id, data in self.runs.items() 
                   if data.get("user_id") == user_id]
        return list(self.runs.keys())
    
    def get_all_runs(self, user_id: Optional[str] = None) -> List[AssistantRun]:
        """Get all runs"""
        runs = []
        for run_id, data in self.runs.items():
            if user_id is None or data.get("user_id") == user_id:
                runs.append(AssistantRun(
                    run_id=run_id,
                    messages=data["messages"],
                    metadata=data["metadata"],
                    user_id=data["user_id"],
                    assistant_name=data["assistant_name"]
                ))
        return runs
    
    def delete(self, run_id: str) -> None:
        """Delete a run"""
        if run_id in self.runs:
            del self.runs[run_id]
    
    def read(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Read a run by ID"""
        if run_id in self.runs:
            return self.runs[run_id]
        return None
    
    def upsert(self, run_id: str, data: Dict[str, Any]) -> None:
        """Update or insert a run"""
        self.runs[run_id] = data 