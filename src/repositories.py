import sqlite3
from personal_data import PersonalData

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

    def get_tags_of_user(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT tags.tag_name
                FROM tags
                JOIN user_tags ON tags.id = user_tags.tag_id
                WHERE user_tags.user_id = ?
            """, (user_id,))
            return cursor.fetchall()

    def get_users_by_tag(self, tag_name: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT users.id, users.username
                FROM users
                JOIN user_tags ON users.id = user_tags.user_id
                JOIN tags ON tags.id = user_tags.tag_id
                WHERE tags.tag_name = ?
            """, (tag_name,))
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

    def is_tag_exist(self, tag_name : str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            conn.execute(
                "SELECT * FROM tags WHERE tag_name=?",
                (tag_name,)
            )
            return cursor.fetchone() is not None

    def add_new_tag(self, tag_name: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO tags (tag_name) VALUES (?)
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