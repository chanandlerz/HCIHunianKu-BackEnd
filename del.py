import sqlite3

conn = sqlite3.connect("userdb.db")
c = conn.cursor()

#username_to_delete = "f7d0e9bae54aa85e"

#delete_statement = f"DELETE FROM post_Forum WHERE udid = '{username_to_delete}'"

delete_statement = "DELETE FROM Register"

c.execute(delete_statement)

conn.commit()

conn.close()
