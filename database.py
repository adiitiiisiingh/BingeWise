import sqlite3

conn = sqlite3.connect("bingewise.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE,
    poster TEXT,
    year TEXT,
    rating TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")