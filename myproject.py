# 📁 server.py -----
import sqlite3
import requests
import http.client
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

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

    #do we do this one or use our schema???
   # conn.row_factory = sqlite3.Row
    return conn

#should be called everytime a user likes a post
def FillUser(name,  email):
    #conn = http.client.HTTPSConnection("www.noahwilliamshaffer.com")

    #headers = { 'authorization': "Bearer {yourMgmtApiAccessToken}" }

    #conn.request("GET", "/var/www/noahwilliamshaffer.com/api/v2/users/%7BuserId%7D", headers=headers)

    #res = conn.getresponse()
    #data = res.read()
    #dictionary = dir(res)    
    #decodedData = data.decode("utf-8")
    #name = session.userinfo.name
    connection = sqlite3.connect('likedArticles.db')
    #EMAIL = decodedData.get('email')
    #do we do this one or sqlite3.Row???
    with open('artSchema.sql') as b:
        connection.executescript(b.read())
        cur = connection.cursor()

        cur.execute("INSERT OR IGNORE INTO users(name, email) VALUES (?, ?)",
        (name, email)
            )

    connection.commit()
    connection.close()

def FillLikedArt(email, title, url):
    #liked articles unique to each user
    connection = sqlite3.connect('likedArticles.db')

    #do we do this one or sqlite3.Row???
    with open('artSchema.sql') as b:
        connection.executescript(b.read())
        cur = connection.cursor()


    cur.execute("INSERT OR INGNORE INTO likedArt (User_Id,title,url) VALUES (?, ?)",
            (email, title, url)
            )
    connection.commit()
    connection.close()

    #for x in range(0, 10):
     #   cur.execute("INSERT INTO likedArt (title, url) VALUES (?, ?)",
      #  ('title', 'url')
       #     )

#    connection.commit()
 #   connection.close()

#FillLikedArt()
def FillDataBase():
    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    )
    link_titles = []    #the emptylist for titles
    link_url = []       #the empty list for url's of hackernews
    #for loop that loops through the ten articles and prints the x title over the x link
    for x in range(0, 30):
        link_string = f"https://hacker-news.firebaseio.com/v0/item/{response.json()[x]}.json?print=pretty"
        link = requests.get(link_string).json()
        link_titles.append(link["title"])
        link_url.append(link["url"])
    con = get_db_connection()
    connection = sqlite3.connect('database.db')

    #do we do this one or sqlite3.Row???
    with open('schema.sql') as f:
        connection.executescript(f.read())
        cur = connection.cursor()

    for x in range(0, 30):
        cur.execute("INSERT INTO Art (title, url) VALUES (?, ?)",
        (link_titles[x], link_url[x])
            )

    connection.commit()
    connection.close()


#FillDataBase()


#the index function contains the way to call the html file that will be using the data being heald in our database ex
#APP ROUTE FUNCTION FOR DATABASE CODE EXSAMPLE
@app.route('/database')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM Art').fetchall()
    conn.close()
    return render_template('database.html', posts=posts)

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

@app.route("/", methods =["GET", "POST"]) #Add a post request
def home():
   # if request.method == "POST":
    #    userName = request.form["name"]
     #   userEmail = request.form["email"]
      #  return render_template("Admin.html",session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4)))
   # else:
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

# 👆 We're continuing from the steps above. Append this to your server.py file.
@app.route("/news", methods =["GET", "POST"])
#Define function for top ten articles
#conn = get_db_connection()
#Art = conn.execute('SELECT * FROM Art').fetchall()
#conn.close()
def show_top_ten():
    #if request.method == "POST":
        #userName = request.form["name"]
        #userEmail = request.form["email"]
        #return render_template("/")
    #else:    
        titles_arr = []
        urls_arr = []
    #connection = sqlite3.connect('database.db')
    #with open('schema.sql') as f:
    #    connection.executescript(f.read())
    #    cur = connection.cursor()
        conn = get_db_connection()
        titles = conn.execute('SELECT title  FROM Art').fetchall()
        urls = conn.execute('SELECT url  FROM Art').fetchall()
        conn.close()

        titles_arr = [i[0] for i in titles]
        urls_arr = [i[0] for i in urls]
    #for row in titles:
     #   titles_arr.append(row[x])

    #for row in urls:
     #   urls_arr.append(row[y])

        #makes the variables available in the html file that this route points to
        return render_template("news.html",titles_arr = titles_arr,urls_arr = urls_arr, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

#In this route, you pass the tuple ('GET', 'POST') to the methods parameter to allow both GET and POST requests.
#GET requests are used to retrieve data from the server.
#POST requests are used to post data to a specific route. 
#By default, only GET requests are allowed.
#When the user first requests the /create route using a GET request, a template file called create.html will be rendered.
#You will later edit this route to handle POST requests for when users fill and submit the web form for creating new posts.
#this is where we we pull from the database


@app.route('/create/', methods=('GET', 'POST'))
def create():
    return render_template('create.html')


@app.route("/oldnews")

def api(): 
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

