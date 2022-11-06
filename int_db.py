import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO Art (title, url) VALUES (?, ?)",
            ('First title', 'first url')
            )

cur.execute("INSERT INTO Art (title, url) VALUES (?, ?)",
            ('Second title', 'second url')
            )

connection.commit()
connection.close()
