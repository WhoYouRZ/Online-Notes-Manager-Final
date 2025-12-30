# app_modules/models.py

from flask_login import UserMixin
from datetime import datetime
from . import get_db


# ============================================================
# USER MODEL
# ============================================================

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = str(id)
        self.username = username
        self.password_hash = password_hash


def get_user_by_id(user_id):
    """Fetch user by primary key."""
    db = get_db()
    row = db.execute(
        "SELECT id, username, password_hash FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()

    if row:
        return User(row["id"], row["username"], row["password_hash"])
    return None


def get_user_by_username(username):
    """Fetch user by username."""
    db = get_db()
    row = db.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,),
    ).fetchone()

    if row:
        return User(row["id"], row["username"], row["password_hash"])
    return None


# ============================================================
# NOTE MODEL / OPERATIONS
# ============================================================

def create_note(user_id, title, content, category_id=None, pinned=False, reminder=None):
    """Create a note for a user."""
    db = get_db()
    db.execute(
        """
        INSERT INTO notes (user_id, title, content, category_id, pinned, reminder, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """,
        (user_id, title, content, category_id, int(pinned), reminder),
    )
    db.commit()


def get_notes_by_user(user_id):
    """Return all notes for a specific user, pinned first."""
    db = get_db()
    rows = db.execute(
        """
        SELECT n.*, c.name AS category_name
        FROM notes n
        LEFT JOIN categories c ON n.category_id = c.id
        WHERE n.user_id = ?
        ORDER BY n.pinned DESC, n.updated_at DESC
        """,
        (user_id,),
    ).fetchall()
    return rows


def get_note_by_id(note_id, user_id):
    """Return a single note owned by the user."""
    db = get_db()
    return db.execute(
        """
        SELECT * FROM notes
        WHERE id = ? AND user_id = ?
        """,
        (note_id, user_id),
    ).fetchone()


def update_note(note_id, user_id, title, content, category_id=None, pinned=False, reminder=None):
    """Update a note."""
    db = get_db()
    db.execute(
        """
        UPDATE notes
        SET title = ?, content = ?, category_id = ?, pinned = ?, reminder = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ? AND user_id = ?
        """,
        (title, content, category_id, int(pinned), reminder, note_id, user_id),
    )
    db.commit()


def delete_note(note_id, user_id):
    """Delete a note."""
    db = get_db()
    db.execute(
        "DELETE FROM notes WHERE id = ? AND user_id = ?",
        (note_id, user_id),
    )
    db.commit()


def search_notes(user_id, query):
    """Search user's notes by title or content."""
    db = get_db()
    like = f"%{query}%"
    return db.execute(
        """
        SELECT n.*, c.name AS category_name
        FROM notes n
        LEFT JOIN categories c ON n.category_id = c.id
        WHERE n.user_id = ?
        AND (n.title LIKE ? OR n.content LIKE ?)
        ORDER BY n.pinned DESC, n.updated_at DESC
        """,
        (user_id, like, like),
    ).fetchall()


# ============================================================
# CATEGORY MODEL
# ============================================================

def create_category(user_id, name):
    db = get_db()
    db.execute(
        "INSERT INTO categories (user_id, name) VALUES (?, ?)",
        (user_id, name),
    )
    db.commit()


def get_categories(user_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM categories WHERE user_id = ? ORDER BY name ASC",
        (user_id,),
    ).fetchall()


# ============================================================
# SYNCING LOCAL NOTES → CLOUD (used in sync.py)
# ============================================================

def insert_synced_note(user_id, title, content, category, created_at):
    """
    Insert a note coming from localStorage during syncing.
    Avoid duplicates by title+content+created_at.
    """
    db = get_db()

    # Check for duplicates
    dup = db.execute(
        """
        SELECT id FROM notes
        WHERE user_id = ? AND title = ? AND content = ? AND created_at = ?
        """,
        (user_id, title, content, created_at),
    ).fetchone()

    if dup:
        return

    db.execute(
        """
        INSERT INTO notes (user_id, title, content, category_id, pinned, reminder, created_at, updated_at)
        VALUES (?, ?, ?, NULL, 0, NULL, ?, CURRENT_TIMESTAMP)
        """,
        (user_id, title, content, created_at),
    )
    db.commit()


# ============================================================
# DATABASE SCHEMA SETUP
# ============================================================

def create_tables(db):
    """
    Creates all required tables.
    Automatically called by `flask init-db`.
    """

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
        """
    )

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT,
            content TEXT,
            category_id INTEGER,
            pinned INTEGER DEFAULT 0,
            reminder TEXT,                 -- stored as ISO timestamp string
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );
        """
    )
    

    db.commit()


__all__ = [
    "User",
    "get_user_by_id",
    "get_user_by_username",
    "create_note",
    "get_notes_by_user",
    "get_note_by_id",
    "update_note",
    "delete_note",
    "search_notes",
    "create_category",
    "get_categories",
    "insert_synced_note",
    "create_tables",
]
