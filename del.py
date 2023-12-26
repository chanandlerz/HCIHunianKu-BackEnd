import sqlite3

conn = sqlite3.connect("userdb.db")
c = conn.cursor()

#username_to_delete = "f7d0e9bae54aa85e"

#delete_statement = f"DELETE FROM post_Forum WHERE udid = '{username_to_delete}'"

delete_statement = "DELETE FROM Register where udid = '987bb52ed20343eb'"''

# sql_statement = "UPDATE Register SET image = NULL WHERE udid = '987bb52ed20343eb'"


c.execute(delete_statement)

conn.commit()

conn.close()
