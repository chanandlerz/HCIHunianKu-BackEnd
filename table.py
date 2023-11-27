import sqlite3

conn = sqlite3.connect("userdb.db")
c = conn.cursor()

#udid, fullName, email, phone, username, password

SQL_STATEMENT = """
CREATE TABLE IF NOT EXISTS users (
    udid VARCHAR(30) PRIMARY KEY,
    username VARCHAR(30),
    password VARCHAR(30)
)
"""

c.execute(SQL_STATEMENT)

conn.commit()
conn.close()