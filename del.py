import sqlite3

conn = sqlite3.connect("userdb.db")
c = conn.cursor()

username_to_delete = "memories"

delete_statement = f"DELETE FROM users WHERE username = '{username_to_delete}'"

c.execute(delete_statement)

conn.commit()

conn.close()
