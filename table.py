import sqlite3

conn = sqlite3.connect("userdb.db")
c = conn.cursor()

#udid, fullName, email, phone, username, password

# ---Register Table---
# SQL_STATEMENT = """
# CREATE TABLE IF NOT EXISTS Register (
#     udid VARCHAR(30),
#     username VARCHAR(30) PRIMARY KEY,
#     password VARCHAR(30),
#     phone VARCHAR(13),
#     email VARCHAR(30),
#     image BLOB
# )
# """


# ---Properties Table---
# SQL_STATEMENT = """
# CREATE TABLE IF NOT EXISTS properties (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     udid VARCHAR(30),
#     action VARCHAR(4),
#     type VARCHAR(10),
#     lokasi VARCHAR(30),
#     harga INT(20),
#     area INT(20),
#     kTidur INT(3),
#     kMandi INT(3),
#     kMandiKos VARCHAR(5),
#     tipeKost VARCHAR(5),
#     ketinggian INT(20),
#     sewa VARCHAR(20),
#     image BLOB,
#     date text,
#     status VARCHAR(4)
# )
# """



# ---Post Forum Table---
# SQL_STATEMENT = """
# CREATE TABLE IF NOT EXISTS Forum (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     udid VARCHAR(30),
#     username VARCHAR(30),
#     caption VARCHAR(300),
#     komen VARCHAR(300),
#     date text,
#     image BLOB
# )
# """

#---Post Komen Table---
# SQL_STATEMENT = """
# CREATE TABLE IF NOT EXISTS komen2 (
#     id INTEGER,
#     udid VARCHAR(30),
#     username VARCHAR(30),
#     komen VARCHAR(300)
# )
# """

# ---Add Column to Table---
SQL_STATEMENT = """
ALTER TABLE properties
ADD desc text;
"""

#---Profile Picture Table---
# SQL_STATEMENT = """
# CREATE TABLE IF NOT EXISTS profile (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     udid VARCHAR(30),
#     image BLOB
# )
# """

c.execute(SQL_STATEMENT)

conn.commit()
conn.close()