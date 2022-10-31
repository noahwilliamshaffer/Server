import sqlite3
import requests

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cursor = connection.cursor()
cursor.execute("CREATE TABLE if not exists Articles (title  TEXT, url  TEXT, number INTEGER)")
#DELETE FROM Articles

cursor.execute("INSERT INTO Articles  VALUES ('title1', 'url1', 1)")
cursor.execute("INSERT INTO Articles VALUES ('title2', 'url2', 2)")

connection.commit()
connection.close()
~                   
