'''This is the server file.'''
import sqlite3

# import http.client
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request

def ClearArticleDatabase():
    connection = sqlite3.connect('/home/marlee/ProjectFiles/database.db')
    with open('/home/marlee/ProjectFiles/schema.sql') as f:
        connection.executescript(f.read())
        cur = connection.cursor()
    cur.execute("DELETE FROM  Art")
    connection.commit()
    connection.close()
ClearArticleDatabase()



def FillDataBase():
    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty"
    )
    link_titles = []    #the emptylist for titles
    link_url = []       #the empty list for url's of hackernews
    #for loop that loops through the ten articles and prints the x title over the x link
    for x in range(0, 40):
        link_string = f"https://hacker-news.firebaseio.com/v0/item/{response.json()[x]}.json?print=pretty"
        link = requests.get(link_string).json()
#some of the articles do not have urls and break the system
        
        if 'url' not in link.keys():
            del link
        else:    
            link_titles.append(link["title"])
            link_url.append(link["url"])
    #con = get_db_connection()
    connection = sqlite3.connect('/home/marlee/ProjectFiles/database.db')

    with open('/home/marlee/ProjectFiles/schema.sql') as f:
        connection.executescript(f.read())
        cur = connection.cursor()

    for x in range(0,30):
        cur.execute("INSERT INTO Art (title, url) VALUES (?, ?)",
        (link_titles[x], link_url[x])
            )

    connection.commit()
    connection.close()
FillDataBase()

