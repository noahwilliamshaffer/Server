# 📁 server.py -----
import sqlite3
import requests
import http.client
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from datetime import timedelta
from flask_sqlalchemy import qlalchemy

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
# 👆 We're continuing from the steps above. Append this to your server.py file.

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
# 👆 We're continuing from the steps above. Append this to your server.py file.

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
# 👆 We're continuing from the steps above. Append this to your server.py file.

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'

)
# 👆 We're continuing from the steps above. Append this to your server.py file.

#get_db_connection is used to make a connection to the database to be able to pull data
#THE DATABASE EXSAMPLE FOR SQLITE CODE ON DIDITAL OCEANS
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
#the index function contains the way to call the html file that will be using the data being heald in our database ex
#APP ROUTE FUNCTION FOR DATABASE CODE EXSAMPLE
@app.route('/database')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route("/login")
def login():
   # return render_template("Login.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )
# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    print("user")
    return redirect("/")
   #return render_template for news.html insted of call back so that the user is logged into the news page
   # return redirect(("/")+ render_template("news.html")) 
# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out!", "info")
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
# 👆 We're continuing from the steps above. Append this to your server.py file.
@app.route("/news")
#Define function for top ten articles
def show_top_ten():
    #response is the .json taken from the hacker news
    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    )
    link_titles = []    #the emptylist for titles
    link_url = []       #the empty list for url's of hackernews
    #for loop that loops through the ten articles and prints the x title over the x link
    for x in range(0, 10):
        link_string = f"https://hacker-news.firebaseio.com/v0/item/{response.json()[x]}.json?print=pretty"
        link = requests.get(link_string).json()
        link_titles.append(link["title"])
        link_url.append(link["url"])
        #makes the variables available in the html file that this route points to
    return render_template("news.html",link_url=link_url, link_titles=link_titles,  session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route("/oldnews")

def api():
    #return render_template("news.html")
    
    #are we sure this is supposed to be client?
    #class http.client.HTTPConnection(host, port=None, [timeout, ]source_address=None, blocksize=8192)¶
    conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")
	
    payload = "{}"
	
    #HTTPConnection.request(method, url, body=None, headers={}, *, encode_chunked=False)
    #try this without payload parameter
    #show marlee definition for body param that we are sending the payload into 
    conn.request("GET", "/v0/topstories.json?print=pretty",payload)
    
    #Should be called after a request is sent to get the response from the server. 
    res = conn.getresponse()
	
    #Reads and returns the response body, or up to the next amt bytes.
    data = res.read()
	
    print(data.decode("utf-8"))

if __name__ == "__main__":
    app.run(debug = True)
