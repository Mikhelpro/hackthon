import sqlite3
from datetime import datetime

DB_PATH = "school_bot.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            name TEXT NOT NULL,
            section TEXT,
            contract_start TEXT,
            contract_end TEXT,
            status TEXT DEFAULT 'active'
        );

        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            name TEXT NOT NULL,
            group_id INTEGER,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            name TEXT
        );

        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER,
            status TEXT,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(teacher_id) REFERENCES teachers(id)
        );

        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            action TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

# --- Teachers ---
def add_teacher(telegram_id, name, section="", contract_start="", contract_end=""):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO teachers (telegram_id, name, section, contract_start, contract_end) VALUES (?,?,?,?,?)",
            (telegram_id, name, section, contract_start, contract_end)
        )
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        conn.close()

def get_teacher(telegram_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM teachers WHERE telegram_id=?", (telegram_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def list_teachers():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM teachers WHERE status='active'").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def remove_teacher(telegram_id):
    conn = get_conn()
    conn.execute("UPDATE teachers SET status='inactive' WHERE telegram_id=?", (telegram_id,))
    conn.commit()
    conn.close()

# --- Groups ---
def add_group(chat_id, name=""):
    conn = get_conn()
    conn.execute("INSERT OR REPLACE INTO groups (chat_id, name) VALUES (?,?)", (chat_id, name))
    conn.commit()
    conn.close()

def list_groups():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM groups").fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- Attendance ---
def log_attendance(teacher_telegram_id, status, note=""):
    conn = get_conn()
    teacher = conn.execute("SELECT id FROM teachers WHERE telegram_id=?", (teacher_telegram_id,)).fetchone()
    if teacher:
        conn.execute(
            "INSERT INTO attendance (teacher_id, status, note) VALUES (?,?,?)",
            (teacher["id"], status, note)
        )
        conn.commit()
    conn.close()

def get_today_attendance():
    conn = get_conn()
    rows = conn.execute("""
        SELECT t.name, t.section, a.status, a.note, a.created_at
        FROM attendance a JOIN teachers t ON a.teacher_id = t.id
        WHERE date(a.created_at) = date('now')
        ORDER BY a.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- Students ---
def register_student(telegram_id, name, group_id=None):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO students (telegram_id, name, group_id) VALUES (?,?,?)",
        (telegram_id, name, group_id)
    )
    conn.commit()
    conn.close()

# --- Logs ---
def add_log(telegram_id, action):
    conn = get_conn()
    conn.execute("INSERT INTO logs (telegram_id, action) VALUES (?,?)", (telegram_id, action))
    conn.commit()
    conn.close()

def get_recent_logs(limit=20):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM logs ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
