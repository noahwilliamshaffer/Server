# 📁 server.py -----
import sqlite3
import requests
import http.client
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, email, EqualTo
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request
from apscheduler.schedulers.background import BackgroundScheduler
#from flask import Flask


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

app.config['SECRET_KEY']  = 'BINGBONG'
class AddLike(FlaskForm):
    title = StringField('Title')
    email = StringField('Email')
    url = StringField('url')
    name = StringField('name')
    submit = SubmitField('Like')
    
class RemoveLike(FlaskForm):
    url = StringField('url')
    submit = SubmitField('Remove')

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)
#Repull the articles every hour

#clear the liked and disliked articles every 24



#get_db_connection is used to make a connection to the database to be able to pull data
#THE DATABASE EXSAMPLE FOR SQLITE CODE ON DIDITAL OCEANS
def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

#should be called everytime a user likes a post
Admins = []
Admins.append("noahwilliamshaffer@gmail.com")
Admins.append("mmk20a@fsu.edu")


def RemoveLikedArt(url_):
    #liked articles unique to each user
    connection = sqlite3.connect('likedArticles.db')
   
    cur = connection.cursor()
    cur.execute("DELETE FROM items WHERE url like '%url_%'")
    connection.commit()
    connection.close()

Url = "Url2"
RemoveLikedArt(Url)



def FillUserEmail(email):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    cur.execute("INSERT OR IGNORE INTO users (email) VALUES (?)",
        (email,))
    connection.commit()
    connection.close()

def initLikedArt():
    connection = sqlite3.connect('likedArticles.db')
    #do we do this one or sqlite3.Row???
    with open('artSchema.sql') as b:
        connection.executescript(b.read())
        cur = connection.cursor()

    connection.commit()
    connection.close()
initLikedArt()

def initDisikedArt():
    connection = sqlite3.connect('dislikedArticles.db')
    #do we do this one or sqlite3.Row???
    with open('disArtSchema.sql') as b:
        connection.executescript(b.read())
        cur = connection.cursor()

    connection.commit()
    connection.close()
initLikedArt()

def FillDislikedArt(name, email, title, url):
    #liked articles unique to each user
    connection = sqlite3.connect('dislikedArticles.db')
    #do we do this one or sqlite3.Row???
    with open('disartSchema.sql') as b:
        connection.executescript(b.read())
        cur = connection.cursor()
    cur.execute("INSERT  OR IGNORE INTO items (list_id, email, title, url) VALUES (?, ?, ?, ?)",
        (name,email, title, url)
            )
    connection.commit()
    connection.close()

def FillLikedArt(name, email, title, url):
    #liked articles unique to each user
    connection = sqlite3.connect('likedArticles.db')
    with open('artSchema.sql') as b:
        connection.executescript(b.read())
        cur = connection.cursor()
    cur.execute("INSERT  OR IGNORE INTO items (list_id, email, title, url) VALUES (?, ?, ?, ?)",
        (name,email, title, url)
            )
    connection.commit()
    connection.close()
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

    with open('schema.sql') as f:
        connection.executescript(f.read())
        cur = connection.cursor()

    for x in range(0, 30):
        cur.execute("INSERT INTO Art (title, url) VALUES (?, ?)",
        (link_titles[x], link_url[x])
            )

    connection.commit()
    connection.close()




@app.route('/removeDislike', methods=['GET', 'POST'])
def removeDislike():
    ID = request.form.get("id")
    con = sqlite3.connect('dislikedArticles.db')
    cursor = con.execute("DELETE FROM items WHERE id = " + ID + ";")
    con.commit()
    cursor = con.execute('SELECT id, email, title, url FROM items')
    Ditems = cursor.fetchall()
    cursor.close()



    Email = request.form.get("email")
    con = sqlite3.connect('likedArticles.db')
    cursor = con.execute('SELECT id, email, title, url FROM items')
    items = cursor.fetchall()
    cursor.close()


    BIG = json.dumps(session.get("user"))
    BIGGER = json.loads(BIG)
    BIGGEST = BIGGER['userinfo']
    EMAIL = BIGGEST['email']
    if EMAIL in Admins:
        return render_template("UserProfiles.html",email = EMAIL,items = items,Ditems = Ditems, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route('/removeLike', methods=['GET', 'POST'])
def removeLike():
    ID = request.form.get("id")
    con = sqlite3.connect('likedArticles.db')
    cursor = con.execute("DELETE FROM items WHERE id = " + ID + ";")
    con.commit()
    cursor = con.execute('SELECT id, email, title, url FROM items')
    items = cursor.fetchall()
    cursor.close()


    Email = request.form.get("email")
    dcon = sqlite3.connect('dislikedArticles.db')
    cursor = dcon.execute('SELECT id, email,title, url FROM items')
    Ditems = cursor.fetchall()
    cursor.close()

    BIG = json.dumps(session.get("user"))
    BIGGER = json.loads(BIG)
    BIGGEST = BIGGER['userinfo']
    EMAIL = BIGGEST['email']
    if EMAIL in Admins:
        return render_template("UserProfiles.html",email = Email,items = items,Ditems = Ditems, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))


@app.route("/UserProfiles", methods =["GET", "POST"])
def UserProfiles():
    Email = request.form.get("email")
    con = sqlite3.connect('likedArticles.db')
    cursor = con.execute('SELECT id, email, title, url FROM items')
    items = cursor.fetchall()
    cursor.close()
    
    Email = request.form.get("email")
    dcon = sqlite3.connect('dislikedArticles.db')
    cursor = dcon.execute('SELECT id, email,title, url FROM items')
    Ditems = cursor.fetchall()
    cursor.close()

    BIG = json.dumps(session.get("user"))
    BIGGER = json.loads(BIG)
    BIGGEST = BIGGER['userinfo']
    EMAIL = BIGGEST['email']
    if EMAIL in Admins:
        return render_template("UserProfiles.html",email = Email,items = items,Ditems = Ditems, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    else:
        return render_template("ErrorAdmin.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
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
    #session["email"] = token
    #print["email"]

    #Delete the database every 24 hours
    #call this every hour
    #FillDataBase() -------------------------------------------------------------------------------------------------------------------------------------
    print("user")
    #Email = "yes@gmail.com"
    BIG = json.dumps(session.get("user"))
    BIGGER = json.loads(BIG)
    BIGGEST = BIGGER['userinfo']
    EMAIL = BIGGEST['email']


    #add user email here
    FillUserEmail(EMAIL)
    #FillUserEmail(Email)
    return redirect("/")

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
#median page distingush likes and disslikes baised on the email that was clicked
@app.route("/Admin")
def Admin():
    EMAIL = "noahwilliamshaffer@gmail.com"
    #EMAIL = "noahwilliamshaffer"
    con = sqlite3.connect('users.db')
    cursor = con.execute('SELECT email, id, created  FROM users')
    items = cursor.fetchall()
    #return render_template('print_items.html', items=items)
    cursor.close()
    if EMAIL in  Admins:
        return render_template("Admin.html",items = items, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    else:
        return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

    

@app.route("/Profile", methods =["GET", "POST"]) #Add a post request
def Profile(): 
    return render_template("Profile.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))


@app.route("/", methods =["GET", "POST"]) #Add a post request
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))



@app.route("/disliked", methods =["GET", "POST"])
def disliked():
    if request.method == "POST":
       # getting input with name = fname in HTML form
        title = request.form["title"]
       # getting input with name = lname in HTML form
        url = request.form["url"]
        #email = requests.form.get("email")
        #name = request.form.get("name")

        #SET NAME AND EMAIL PYTHON SIDE
        BIG = json.dumps(session.get("user"))
        BIGGER = json.loads(BIG)
        BIGGEST = BIGGER['userinfo']
        EMAIL = BIGGEST['email']
        name ="Working"
        FillDislikedArt(name, EMAIL, title, url)
    form = AddLike()
    Email = "Admin2@gmail.com"
    Title ="Title"
    Url = "Url"
    titles_arr = []
    urls_arr = []
    conn = get_db_connection()
    titles = conn.execute('SELECT title  FROM Art').fetchall()
    urls = conn.execute('SELECT url  FROM Art').fetchall()
    conn.close()

    titles_arr = [i[0] for i in titles]
    urls_arr = [i[0] for i in urls]
    #for row in titles:

        #makes the variables available in the html file that this route points to
    return render_template("news.html",titles_arr = titles_arr,urls_arr = urls_arr,form = form, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

#stores it when an article is liked maybey get rig of the route becase this is deals with data may be a way to streemline.
@app.route("/liked", methods =["GET", "POST"])
def liked():
    if request.method == "POST":
       # getting input with name = fname in HTML form
        title = request.form["title"]

       # getting input with name = lname in HTML form
        url = request.form["url"]

        BIG = json.dumps(session.get("user"))
        BIGGER = json.loads(BIG)
        BIGGEST = BIGGER['userinfo']
        EMAIL = BIGGEST['email']
        name ="Working"
        FillLikedArt(name, EMAIL, title, url)
    form = AddLike()
    Email = "Admin2@gmail.com"
    Title ="Title"
    Url = "Url"
    titles_arr = []
    urls_arr = []
    conn = get_db_connection()
    titles = conn.execute('SELECT title  FROM Art').fetchall()
    urls = conn.execute('SELECT url  FROM Art').fetchall()
    conn.close()

    titles_arr = [i[0] for i in titles]
    urls_arr = [i[0] for i in urls]
    return render_template("news.html",titles_arr = titles_arr,urls_arr = urls_arr,form = form, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

# show top 10 is our news rout and site that pulls from api no longer top 10mthough
# 👆 We're continuing from the steps above. Append this to your server.py file.
@app.route("/news", methods =["GET", "POST"])
def show_top_ten():
    form = AddLike()
    Email = "Admin2@gmail.com"
    Title ="Title"
    Url = "Url"
    titles_arr = []
    urls_arr = []
    conn = get_db_connection()
    titles = conn.execute('SELECT title  FROM Art').fetchall()
    urls = conn.execute('SELECT url  FROM Art').fetchall()
    conn.close()

    titles_arr = [i[0] for i in titles]
    urls_arr = [i[0] for i in urls]
    return render_template("news.html",titles_arr = titles_arr,urls_arr = urls_arr,form = form, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

#In this route, you pass the tuple ('GET', 'POST') to the methods parameter to allow both GET and POST requests.
#GET requests are used to retrieve data from the server.
#POST requests are used to post data to a specific route. 
#By default, only GET requests are allowed.
#When the user first requests the /create route using a GET request, a template file called create.html will be rendered.
#You will later edit this route to handle POST requests for when users fill and submit the web form for creating new posts.
#this is where we we pull from the database

##delete funct.
##@app.route('/create/', methods=('GET', 'POST'))
##def create():
  ##  return render_template('create.html')

##old function don't need most likely
##@app.route("/oldnews")

##def api(): 
    #are we sure this is supposed to be client?
    #class http.client.HTTPConnection(host, port=None, [timeout, ]source_address=None, blocksize=8192)¶
   # conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")
	
   # payload = "{}"
	
    #HTTPConnection.request(method, url, body=None, headers={}, *, encode_chunked=False)
    #try this without payload parameter
    #show marlee definition for body param that we are sending the payload into 
   # conn.request("GET", "/v0/topstories.json?print=pretty",payload)
    
    #Should be called after a request is sent to get the response from the server. 
   # res = conn.getresponse()
	
    #Reads and returns the response body, or up to the next amt bytes.
  #  data = res.read()
	
   # print(data.decode("utf-8"))

if __name__ == "__main__":
    app.run(debug = True)

