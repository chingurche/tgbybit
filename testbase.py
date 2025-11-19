import sqlite3

class UserRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT,
            student_group INTEGER
        )
        """)
        conn.commit()
        conn.close()

    def add_or_update_user(self, user_id: int, username: str, student_group: int = None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users (id, username, student_group) VALUES (?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            username = excluded.username,
            student_group = excluded.student_group
        """, (user_id, username, student_group))
        conn.commit()
        conn.close()

    def get_user(self, user_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    def set_student_group(self, user_id: int, student_group: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET student_group=? WHERE id=?", (student_group, user_id))
        conn.commit()
        conn.close()
    
    def get_random_user(self, user_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, student_group 
            FROM users 
            WHERE id != ?
            ORDER BY RANDOM() 
            LIMIT 1
        """, (user_id,))
        row = cursor.fetchone()
        conn.close()
        return row  # tuple или None