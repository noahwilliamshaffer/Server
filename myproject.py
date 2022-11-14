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
# 👆 We're continuing from the steps above. Append this to your server.py file.

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
# 👆 We're continuing from the steps above. Append this to your server.py file.

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
# 👆 We're continuing from the steps above. Append this to your server.py file.

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
# 👆 We're continuing from the steps above. Append this to your server.py file.

#get_db_connection is used to make a connection to the database to be able to pull data
#THE DATABASE EXSAMPLE FOR SQLITE CODE ON DIDITAL OCEANS
def get_db_connection():
    conn = sqlite3.connect('database.db')
    #do we do this one or use our schema???
    #conn.row_factory = sqlite3.Row
    return conn

#should be called everytime a user likes a post
Admins = []
Admins.append("noahwilliamshaffer@gmail.com")

#def FillUser(Id, name, email):
    #email = "Admin@gmail.com"
    #name = "UsersName"
    #conn = http.client.HTTPSConnection("www.noahwilliamshaffer.com")
 
    #headers = { 'authorization': "Bearer {yourMgmtApiAccessToken}" }
 
    #conn.request("GET", "/var/www/noahwilliamshaffer.com/api/v2/users/%7BuserId%7D", headers=headers)
 
    #res = conn.getresponse()
    #data = res.read()
    #dictionary = dir(res)    
    #decodedData = data.decode("utf-8")
    #name = session.userinfo.name
    #connection = sqlite3.connect('likedArticles.db')
    #EMAIL = decodedData.get('email')
    #do we do this one or sqlite3.Row???
 #   with open('artSchema.sql') as b:
  #      connection.executescript(b.read())
   #     cur = connection.cursor()
 
   # cur.execute("INSERT INTO usr (id, email) VALUES (?,?)", (111111,'bingo@gmail.com'))
   # cur.execute("INSERT INTO usr (id, email) VALUES (?, ?)", (222222, 'bingbong@gmail.com'))
   # cur.execute("INSERT INTO usr (id, email) VALUES (?, ?)", (333333,'santa@gmail.com'))
 
        #SET IDENTITY_INSERT users ON;
        #cur.execute("INSERT INTO users(name, email) VALUES ( ?, ?)",
        #( name, email)
         #   )
 
    #connection.commit()
    #connection.close()
#Id = 3;
#Email = "Admin3@gmail.com"
#Name = "User3Name"
#FillUser(Id,Name,Email)


def RemoveLikedArt(url_):
    #liked articles unique to each user
    connection = sqlite3.connect('likedArticles.db')
    #do we do this one or sqlite3.Row???
    with open('artSchema.sql') as b:
        connection.executescript(b.read())
        cur = connection.cursor()
    #cur.execute("INSERT OR IGNORE INTO likedArt (ID,title, url) VALUES (?,?, ?)",
    #        (Id,title, url)
    #
    cur.execute("DELETE FROM items WHERE url like '%url_%'")
    connection.commit()
    connection.close()

Url = "Url2"
RemoveLikedArt(Url)



def FillUserEmail(email):
    connection = sqlite3.connect('users.db')
    with open('emails.sql') as x:
        connection.executescript(x.read())
        cur = connection.cursor()
    cur.execute("INSERT INTO users (email) VALUES (?)",
        (email,))
    cur.execute("INSERT INTO users (email) VALUES (?)",
        ('example1@gmail.com',))
    cur.execute("INSERT INTO users (email) VALUES (?)",
        ('example2@gmail.com',))
    cur.execute("INSERT INTO users (email) VALUES (?)",
        ('example3@gmail.com',))
    cur.execute("INSERT INTO users (email) VALUES (?)",
        ('example4@gmail.com',))
    cur.execute("INSERT INTO users (email) VALUES (?)",
        ('example5@gmail.com',))
    connection.commit()
    connection.close()
email = "GOLLYGWILIKERS@gmail.com"
FillUserEmail(email)



def FillLikedArt(name, email, title, url):
    #liked articles unique to each user
    connection = sqlite3.connect('likedArticles.db')
    #do we do this one or sqlite3.Row???
    with open('artSchema.sql') as b:
        connection.executescript(b.read())
        cur = connection.cursor()
    #cur.execute("INSERT OR IGNORE INTO likedArt (ID,title, url) VALUES (?,?, ?)",
    #        (Id,title, url)
    #      
    cur.execute("INSERT INTO items (list_id, email, title, url) VALUES (?, ?, ?, ?)",
        (name,email, title, url)
            )
    cur.execute("INSERT INTO items (list_id, email, title, url) VALUES (?, ?, ?, ?)",
        (111111,'Example5@gmail.com', 'TITLE1', 'www.example1.com')
            )
 
    cur.execute("INSERT INTO items (list_id, email, title, url) VALUES (?,?, ?, ?)",
            (222222,'Example5@gmail.com', 'TITLE2', 'www.example2.com')
            )
 
    cur.execute("INSERT INTO items (list_id, email, title, url) VALUES (?, ?, ?, ?)",
            (222222,'Example5@gmail.com', 'TITLE3', 'www.example3.com')
            )
 
    cur.execute("INSERT INTO items (list_id, email, title, url) VALUES (?, ?, ?, ?)",
            (333333,'Example5@gmail.com', 'TITLE4', 'www.example4.com')
            )
 
    cur.execute("INSERT INTO items (list_id, email, title, url) VALUES (?, ?, ?, ?)",
            (333333, 'Example5@gmail.com', 'TITLE5', 'www.example5.com')
            )
    connection.commit()
    connection.close()
name ="noah"
email = "Admin3@gmail.com"
Title ="Title2"
Url = "BINGOBANGO.com"
FillLikedArt(name,email,Title,Url)


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

@app.route('/Like', methods=['GET', 'POST'])
def Like():
    #output = request.form.to_dict()
    #title = output["title"]


    return redirect("/news")


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    output = request.form.to_dict()
    name = output["name"]

@app.route("/UserProfiles", methods =["GET", "POST"])
def UserProfiles():
    if request.method == "POST":
       # getting input with name = fname in HTML form
        ID = request.form.get("id")
        con = sqlite3.connect('likedArticles.db')
        cursor = con.execute('DELETE FROM items WHERE id = ID')
        items = cursor.fetchall()
        cursor.close()
        #BIG=session.get('user')
        #Email = BIG.userinfo.name
    #Email = session.userinfo.name
    Email = request.form.get("email")
    con = sqlite3.connect('likedArticles.db')
    cursor = con.execute('SELECT id, title, url FROM items WHERE email = Email')
    items = cursor.fetchall()
    cursor.close()

    return render_template("UserProfiles.html",email = Email,items = items, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
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

@app.route("/Admin")
def Admin():
    EMAIL = "noahwilliamshaffer"
    con = sqlite3.connect('users.db')
    cursor = con.execute('SELECT email, id, created  FROM users')
    items = cursor.fetchall()
    #return render_template('print_items.html', items=items)
    cursor.close()
    if EMAIL in  Admins:
        return render_template("Admin.html",items = items, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    else:
        return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

    
# 👆 We're continuing from the steps above. Append this to your server.py file.

#@app.route("/Admin", methods =["GET", "POST"])
#def Admin():
#    return render_template("Admin.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route("/", methods =["GET", "POST"]) #Add a post request
def home():
    Email = "noahwilliamshaffer@gmail.com"
    #userinfo = json.dumps(session.get("user"))
    #temp = json.loads(userinfo)
    #temp2 = temp['userinfo']
    #ids = temp2['sub']i

    #add user email here
    FillUserEmail(email)


    #connect to user emails here
    #con = sqlite3.connect('emails.db')
    #cursor = con.execute('SELECT email FROM users')

    #con = sqlite3.connect('likedArticles.db')
    #cursor = con.execute('SELECT title,email,url FROM items')
    con = sqlite3.connect('users.db')
    cursor = con.execute('SELECT email, id, created  FROM users')
    items = cursor.fetchall()
    #return render_template('print_items.html', items=items)
    cursor.close()
    if Email in  Admins:
        #def printLiked():
            #con = sqlite3.connect('likedArticles.db')
            #with open('artSchema.sql') as f:
             #   con.executescript(f.read())
           # cur = con.cursor
            #conn = get_db_connection()
            #emails = con.execute('SELECT email FROM items').fetchall()
            #conn.close()

            #emails_arr = [i[0] for i in emails]

        return render_template("Admin.html",items = items, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    
    else:
        return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))


#@app.route("/Liked", methods =["GET", "POST"])
#def show_top_ten():
#    Email = "Admin2@gmail.com"
#    Title ="Title"
#    Url = "Url"

#return render_template("Liked.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))


# 👆 We're continuing from the steps above. Append this to your server.py file.
@app.route("/news", methods =["GET", "POST"])
#form = AddLike()
#Define function for top ten articles
#conn = get_db_connection()
#Art = conn.execute('SELECT * FROM Art').fetchall()
#conn.close()
def show_top_ten():
    if request.method == "POST":
       # getting input with name = fname in HTML form
        title = request.form.get("title")
       # getting input with name = lname in HTML form
        url = request.form.get("url")
        #email = requests.form.get("email")
        #name = request.form.get("name")
        
        #SET NAME AND EMAIL PYTHON SIDE
        email = "ThisWorks@gmail.com"
        name ="Working"
        FillLikedArt(name, email, title, url)
    form = AddLike()
    Email = "Admin2@gmail.com"
    Title ="Title"
    Url = "Url"
    #FillLikedArt(Email,Title,Url)
    #if request.method == "POST":
        #userName = request.form["name"]
        #userEmail = request.form["email"]
        #return render_template("/")
    #else:    
    titles_arr = []
    urls_arr = []
    #I DONT KNOW WHY THIS IS COMMENTED OUT I REMEMBER NEEDING TO USE THIS
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
   # output = request.form.to_dict()
    #title = output["title"]
        #makes the variables available in the html file that this route points to
    return render_template("news.html",titles_arr = titles_arr,urls_arr = urls_arr,form = form, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

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

