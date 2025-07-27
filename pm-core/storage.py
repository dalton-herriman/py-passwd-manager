import sqlite3
from typing import Any, List, Tuple, Optional

class SQLiteStorage:
    def __init__(self, db_path: str = "pm_data.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        # Example table for storing key-value pairs (customize as needed)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def set(self, key: str, value: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO data (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))
        self.conn.commit()

    def get(self, key: str) -> Optional[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM data WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else None

    def delete(self, key: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM data WHERE key = ?", (key,))
        self.conn.commit()

    def list_keys(self) -> List[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT key FROM data")
        return [row[0] for row in cursor.fetchall()]

    def close(self):
        self.conn.close()

# Example usage:
# storage = SQLiteStorage()
# storage.set("username", "alice")
# print(storage.get("username"))
# storage.delete("username")
# storage.close()
