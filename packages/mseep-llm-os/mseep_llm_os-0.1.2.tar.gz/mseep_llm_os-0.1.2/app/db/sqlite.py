import os
import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from .base import BaseStorage
from .config import db_settings

class SQLiteStorage(BaseStorage):
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
    
    def save_run(
        self,
        run_id: str,
        messages: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        assistant_name: Optional[str] = None,
    ) -> None:
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
    
    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
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