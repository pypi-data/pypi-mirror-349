import os
from typing import Optional, Union, List, Dict, Any
from pathlib import Path
import sqlite3
import json
from datetime import datetime
from phi.storage.assistant.base import AssistantStorage as PhiAssistantStorage
from phi.storage.assistant.postgres import PgAssistantStorage
from .config import db_settings
from .init import init_database
import logging
from phi.assistant import AssistantRun

logger = logging.getLogger(__name__)

class SQLiteStorage:
    def __init__(self, db_path: Optional[str] = None):
        """Initialize SQLite storage"""
        if db_path is None:
            db_path = db_settings.absolute_db_path
        
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
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
    
    def save_run(self, run_id: str, messages: list, metadata: dict = None, user_id: str = None, assistant_name: str = None):
        """Save a conversation run"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO assistant_runs 
                (run_id, user_id, assistant_name, created_at, messages, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    user_id,
                    assistant_name,
                    datetime.utcnow().isoformat(),
                    json.dumps(messages),
                    json.dumps(metadata or {})
                )
            )
            conn.commit()
    
    def get_run(self, run_id: str) -> Optional[dict]:
        """Get a conversation run by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM assistant_runs WHERE run_id = ?",
                (run_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return {
                    "run_id": row["run_id"],
                    "user_id": row["user_id"],
                    "assistant_name": row["assistant_name"],
                    "created_at": row["created_at"],
                    "messages": json.loads(row["messages"]),
                    "metadata": json.loads(row["metadata"])
                }
            return None 
    
    def delete_run(self, run_id: str) -> None:
        """Delete a conversation run"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM assistant_runs WHERE run_id = ?", (run_id,))
            conn.commit()
    
    def get_all_runs(self) -> List[Dict[str, Any]]:
        """Get all conversation runs"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM assistant_runs ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            return [
                {
                    "run_id": row["run_id"],
                    "user_id": row["user_id"],
                    "assistant_name": row["assistant_name"],
                    "created_at": row["created_at"],
                    "messages": json.loads(row["messages"]),
                    "metadata": json.loads(row["metadata"])
                }
                for row in rows
            ]
    
    def get_all_run_ids(self) -> List[str]:
        """Get all run IDs"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT run_id FROM assistant_runs ORDER BY created_at DESC")
            return [row[0] for row in cursor.fetchall()]

def get_storage() -> PhiAssistantStorage:
    """Get the appropriate storage implementation based on configuration"""
    # Initialize database if auto-create is enabled
    if not init_database():
        raise RuntimeError("Failed to initialize database. Check logs for details.")
    
    try:
        if db_settings.is_sqlite:
            # Delay import to avoid circular dependency
            from ai.storage import SQLiteAssistantStorage
            storage = SQLiteAssistantStorage()
            # Test database connection
            storage.get_all_run_ids()  # If database has issues, this will raise an exception
            return storage
        elif db_settings.is_postgres:
            storage = PgAssistantStorage(
                table_name="lyraios_storage",
                db_url=db_settings.db_url
            )
            # Test database connection
            storage.get_all_run_ids()
            return storage
        else:
            raise ValueError(f"Unsupported database type: {db_settings.DATABASE_TYPE}")
    except Exception as e:
        logger.error(f"Failed to create storage: {e}")
        raise RuntimeError("[storage] Could not create assistant, is the database running?")

class AssistantStorage(PhiAssistantStorage):
    """Assistant storage implementation"""
    
    def __init__(self):
        """Initialize storage"""
        self.runs = {}  # In-memory storage for development
    
    def create(self, messages: List[Dict[str, Any]], metadata: Dict[str, Any], 
               user_id: Optional[str] = None, assistant_name: str = "LYRAIOS") -> str:
        """Create a new run"""
        run_id = f"run_{len(self.runs) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
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