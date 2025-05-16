import os
import sqlite3
import threading
import time
import shutil
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

class LocalDB:
    def __init__(self, db_path: str = None, backup_interval: int = 3600):
        data_dir = os.path.join(os.getcwd(), 'data')
        backup_dir = os.path.join(data_dir, 'db_rl')
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(backup_dir, exist_ok=True)
        self.db_path = db_path or os.path.join(data_dir, 'zone_db.sqlite3')
        self.backup_dir = backup_dir
        self.backup_interval = backup_interval
        self._lock = threading.Lock()
        self._init_db()
        self._start_backup_thread()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS shuoshuo (
                key INTEGER PRIMARY KEY AUTOINCREMENT,
                id TEXT,
                qq TEXT,
                content TEXT,
                is_forward BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
            conn.commit()

    def add_shuoshuo(self, qq: str, shuoshuo_id: str, content: Dict[str, Any], is_forward: bool = False):
        with self._lock, sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT OR IGNORE INTO shuoshuo (id, qq, content, is_forward) VALUES (?, ?, ?, ?)''',
                      (shuoshuo_id, qq, json.dumps(content, ensure_ascii=False), int(is_forward)))
            conn.commit()

    def get_all_ids(self, qq: str) -> List[str]:
        with self._lock, sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM shuoshuo WHERE qq = ?', (qq,))
            return [row[0] for row in c.fetchall()]

    def get_shuoshuo(self, qq: str, shuoshuo_id: str) -> Optional[Dict[str, Any]]:
        with self._lock, sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT content FROM shuoshuo WHERE qq = ? AND id = ?', (qq, shuoshuo_id))
            row = c.fetchone()
            if row:
                return json.loads(row[0])
            return None

    def _backup(self):
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'zone_db_backup_{now}.sqlite3')
        with self._lock:
            shutil.copy2(self.db_path, backup_file)

    def _start_backup_thread(self):
        def backup_loop():
            while True:
                time.sleep(self.backup_interval)
                self._backup()
        t = threading.Thread(target=backup_loop, daemon=True)
        t.start()

    def set_backup_interval(self, interval: int):
        self.backup_interval = interval

db = LocalDB(backup_interval=86400)