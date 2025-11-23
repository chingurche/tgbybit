import sqlite3
from models import PersonalData

class ConnectionsRepository:
    def __init__(self, db_path : str):
        self.db_path = db_path
        #self._create_table()

    def _create_table(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user INTEGER NOT NULL,
                to_user INTEGER NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('pending', 'accepted', 'declined')) DEFAULT 'pending',

                FOREIGN KEY (from_user) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (to_user) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

    def create_request(self, from_user: int, to_user: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO connections (from_user, to_user) VALUES (?, ?)",
                (from_user, to_user)
            )
            return cursor.lastrowid

    def accept_request(self, request_id: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE connections SET status='accepted' WHERE id=?",
                (request_id,)
            )

    def decline_request(self, request_id: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE connections SET status='declined' WHERE id=?",
                (request_id,)
            )

    def get_pending_for_user(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, from_user FROM connections WHERE to_user=? AND status='pending'",
                (user_id,)
            )
            return cursor.fetchall()

class UserTagsRepository:
    def __init__(self, db_path : str):
        self.db_path = db_path
        self._create_table()

    def _create_table(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_tags (
                user_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(tag_id) REFERENCES tags(id),
                PRIMARY KEY(user_id, tag_id)
            )
            """)

    def add_tag_to_user(self, user_id: int, tag_id: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO user_tags (user_id, tag_id) VALUES (?, ?)",
                (user_id, tag_id)
            )

    def remove_tag_from_user(self, user_id: int, tag_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                DELETE FROM user_tags 
                WHERE user_id = ? AND tag_id = ?
            """, (user_id, tag_id))

            return cursor.rowcount > 0 

    def get_tags_of_user(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT tags.tag_name
                FROM tags
                JOIN user_tags ON tags.id = user_tags.tag_id
                WHERE user_tags.user_id = ?
            """, (user_id,))
            return cursor.fetchall()

    def get_users_by_tag(self, tag_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT users.id
                FROM users
                JOIN user_tags ON users.id = user_tags.user_id
                WHERE user_tags.tag_id = ?
            """, (tag_id,))
            return cursor.fetchall()
    
    
    def get_top_tags(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT t.tag_name, COUNT(ut.user_id) AS user_count
                FROM user_tags ut
                JOIN tags t ON ut.tag_id = t.id
                GROUP BY ut.tag_id
                ORDER BY user_count DESC
                LIMIT 5;
            """)
            return cursor.fetchall()

class TagsRepository:
    def __init__(self, db_path : str):
        self.db_path = db_path
        self._create_table()

    def _create_table(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tags(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag_name TEXT UNIQUE
            )
            """)

    """def is_tag_exist(self, tag_name : str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            conn.execute(
                "SELECT * FROM tags WHERE tag_name=?",
                (tag_name,)
            )
            return cursor.fetchone() is not None"""
        
    def get_tag_id(self, tag_name : str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tags.id
                FROM tags
                WHERE tag_name=?""",
                (tag_name,)
            )
            return cursor.fetchone()[0]

    def add_new_tag(self, tag_name: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR IGNORE INTO tags (tag_name) VALUES (?)
                """,
                (tag_name,)
            )

class UserRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                username TEXT,
                student_group INTEGER
            )
            """)

    def add_or_update_user(self, user_id: int, data : PersonalData):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            INSERT INTO users (id, username, student_group) VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                username = excluded.username,
                student_group = excluded.student_group
            """, (user_id, data.name, data.student_group))

    def get_user(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE id=?",
                (user_id,)
            )
            return cursor.fetchone()
    
    def get_random_user_id(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id 
                FROM users 
                WHERE id != ?
                ORDER BY RANDOM()
                LIMIT 1
            """, (user_id,))
            return cursor.fetchone()[0]

    """def set_student_group(self, user_id: int, student_group: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE users SET student_group=? WHERE id=?",
                (student_group, user_id)
            )"""