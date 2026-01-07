import sqlite3

conn = sqlite3.connect("todo.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER NOT NULL
)
""")
conn.close()
print("Database created successfully")