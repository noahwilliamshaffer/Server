# 📁 server.py -----
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
from apscheduler.schedulers.background import BackgroundScheduler

# from flask import Flask


env_file = find_dotenv()
if env_file:
    load_dotenv(env_file)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

app.config["SECRET_KEY"] = "BINGBONG"


class AddLike(FlaskForm):
    """class for adding likes"""

    title = StringField("Title")
    email = StringField("Email")
    url = StringField("url")
    name = StringField("name")
    submit = SubmitField("Like")


class RemoveLikeForm(FlaskForm):
    """ removes likes class"""

    url = StringField("url")
    submit = SubmitField("Remove")


oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email",},
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# Repull the articles every hour

# clear the liked and disliked articles every 24


def clear_and_fill_article_databases():
    """This clears and fills the article databases."""
    connection = sqlite3.connect("database.db")

    with open("schema.sql") as f:
        connection.executescript(f.read())
        cur = connection.cursor()

    cur.execute("DELETE FROM  Art")

    connection.commit()
    connection.close()
    fill_data_base()


def clear_liked_art():
    connection = sqlite3.connect("likedArticles.db")

    cur = connection.cursor()
    cur.execute(" DELETE FROM items")
    connection.commit()
    connection.close()


def clear_disliked_art():
    connection = sqlite3.connect("likedArticles.db")

    cur = connection.cursor()
    cur.execute(" DELETE FROM items")
    connection.commit()
    connection.close()


def sensor():
    """Function for test purposes."""
    print("Scheduler is alive!")


sched = BackgroundScheduler(daemon=True)
sched.add_job(clear_liked_art, "interval", minutes=60)
sched.add_job(clear_disliked_art, "interval", minutes=60)
sched.add_job(clear_and_fill_article_databases, "interval", hours=24)
sched.start()


# get_db_connection is used to make a connection to the database to be able to pull data
# THE DATABASE EXSAMPLE FOR SQLITE CODE ON DIDITAL OCEANS
def get_db_connection():
    conn = sqlite3.connect("database.db")
    return conn

# should be called everytime a user likes a post
Admins = []
Admins.append("noahwilliamshaffer@gmail.com")
Admins.append("mmk20a@fsu.edu")
Admins.append("chashimahiulislam@gmail.com")

# def remove_liked_art(url_):
def remove_liked_art():
    '''This removes liked art from the database.'''
    # liked articles unique to each user
    connection = sqlite3.connect("likedArticles.db")

    cur = connection.cursor()
    cur.execute("DELETE FROM items WHERE url like '%url_%'")
    connection.commit()
    connection.close()

URL = "Url2"
remove_liked_art(URL)

def fill_user_email(email):
    '''This puts the user email in the database.'''
    connection = sqlite3.connect("users.db")
    cur = connection.cursor()
    cur.execute("INSERT OR IGNORE INTO users (email) VALUES (?)", (email,))
    connection.commit()
    connection.close()


def init_liked_art():
    """This inits the liked art database."""
    connection = sqlite3.connect("likedArticles.db")
    # do we do this one or sqlite3.Row???
    with open("artSchema.sql") as b_var:
        connection.executescript(b_var.read())
        # cur = connection.cursor()
        connection.cursor()

    connection.commit()
    connection.close()


init_liked_art()


def init_disiked_art():
    """This inits the disliked art database."""
    connection = sqlite3.connect("dislikedArticles.db")
    # do we do this one or sqlite3.Row???
    with open("disArtSchema.sql") as b_var:
        connection.executescript(b_var.read())
        # cur = connection.cursor()
        connection.cursor()

    connection.commit()
    connection.close()


init_liked_art()


def fill_disliked_art(name, email, title, url):
    """This fills the disliked art database."""
    # liked articles unique to each user
    connection = sqlite3.connect("dislikedArticles.db")
    # do we do this one or sqlite3.Row???
    with open("disartSchema.sql") as b_var:
        connection.executescript(b_var.read())
        cur = connection.cursor()
    cur.execute(
        "INSERT  OR IGNORE INTO items (list_id, email, title, url) VALUES (?, ?, ?, ?)",
        (name, email, title, url),
    )
    connection.commit()
    connection.close()


def fill_liked_art(name, email, title, url):
    """This fills the liked art database."""
    # liked articles unique to each user
    connection = sqlite3.connect("likedArticles.db")
    with open("artSchema.sql") as b_var:
        connection.executescript(b_var.read())
        cur = connection.cursor()
    cur.execute(
        "INSERT  OR IGNORE INTO items (list_id, email, title, url) VALUES (?, ?, ?, ?)",
        (name, email, title, url),
    )
    connection.commit()
    connection.close()


def fill_data_base():
    """This fills the database."""
    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    )
    link_titles = []  # the emptylist for titles
    link_url = []  # the empty list for url's of hackernews
    # for loop that loops through the ten articles and prints the x title over the x link
    for x_var in range(0, 30):
        link_string = (
            f"https://hacker-news.firebaseio.com/v0/item/"
            f"{response.json()[x_var]}.json?print=pretty"
        )
        link = requests.get(link_string).json()
        link_titles.append(link["title"])
        link_url.append(link["url"])
    # con = get_db_connection()
    get_db_connection()
    connection = sqlite3.connect("database.db")

    with open("schema.sql") as f:
        connection.executescript(f.read())
        cur = connection.cursor()

    for x_var in range(0, 30):
        cur.execute(
            "INSERT INTO Art (title, url) VALUES (?, ?)",
            (link_titles[x_var], link_url[x_var]),
        )

    connection.commit()
    connection.close()


@app.route("/removeDislike", methods=["GET", "POST"])
def remove_dislike():
    # i_d = request.form.get("id")
    con = sqlite3.connect("dislikedArticles.db")
    cursor = con.execute("DELETE FROM items WHERE id = " + id + ";")
    con.commit()
    cursor = con.execute("SELECT id, email, title, url FROM items")
    d_items = cursor.fetchall()
    cursor.close()

    # email = request.form.get("email")
    con = sqlite3.connect("likedArticles.db")
    cursor = con.execute("SELECT id, email, title, url FROM items")
    items = cursor.fetchall()
    cursor.close()

    big = json.dumps(session.get("user"))
    bigger = json.loads(big)
    biggest = bigger["userinfo"]
    e_mail = biggest["email"]
    if e_mail in Admins:
        return render_template(
            "UserProfiles.html",
            email=e_mail,
            items=items,
            Ditems=d_items,
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )


@app.route("/removeLike", methods=["GET", "POST"])
def remove_like():
    """This removes a like from a post."""
    i_d = request.form.get("id")
    con = sqlite3.connect("likedArticles.db")
    cursor = con.execute("DELETE FROM items WHERE id = " + i_d + ";")
    con.commit()
    cursor = con.execute("SELECT id, email, title, url FROM items")
    items = cursor.fetchall()
    cursor.close()

    emai_l = request.form.get("email")
    dcon = sqlite3.connect("dislikedArticles.db")
    cursor = dcon.execute("SELECT id, email,title, url FROM items")
    d_items = cursor.fetchall()
    cursor.close()

    bi_g = json.dumps(session.get("user"))
    bigge_r = json.loads(bi_g)
    bigges_t = bigge_r["userinfo"]
    e_mail = bigges_t["email"]
    if e_mail in Admins:
        return render_template(
            "UserProfiles.html",
            email=emai_l,
            items=items,
            Ditems=d_items,
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )


@app.route("/UserProfiles", methods=["GET", "POST"])
def user_profiles():
    """This pulls the user profile data."""
    email = request.form.get("email")
    con = sqlite3.connect("likedArticles.db")
    cursor = con.execute("SELECT id, email, title, url FROM items")
    items = cursor.fetchall()
    cursor.close()

    email = request.form.get("email")
    dcon = sqlite3.connect("dislikedArticles.db")
    cursor = dcon.execute("SELECT id, email,title, url FROM items")
    d_items = cursor.fetchall()
    cursor.close()

    big = json.dumps(session.get("user"))
    bigger = json.loads(big)
    biggest = bigger["userinfo"]
    e_mail = biggest["email"]
    if e_mail in Admins:
        return render_template(
            "UserProfiles.html",
            email=email,
            items=items,
            Ditems=d_items,
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
    else:
        return render_template(
            "ErrorAdmin.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )


# the index function contains the way to call the
# html file that will be using the data being heald in our database ex
# APP ROUTE FUNCTION FOR DATABASE CODE EXSAMPLE
@app.route("/database")
def index():
    """ sends information and runs database.html"""
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM Art").fetchall()
    conn.close()
    return render_template("database.html", posts=posts)


@app.route("/login")
def login():
    """runs and authenticates login page"""
    # return render_template("Login.html", session=session.get('user')
    # , pretty=json.dumps(session.get('user'), indent=4))
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


# 👆 We're continuing from the steps above. Append this to your server.py file.


@app.route("/callback", methods=["GET", "POST"])
def callback():
    """ runs callback page and authenticates"""
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    # session["email"] = token
    # print["email"]

    # Delete the database every 24 hours
    # call this every hour
    # FillDataBase()
    print("user")
    # Email = "yes@gmail.com"
    big = json.dumps(session.get("user"))
    bigger = json.loads(big)
    biggest = bigger["userinfo"]
    e_mail = biggest["email"]

    # add user email here
    fill_user_email(e_mail)
    # FillUserEmail(Email)
    return redirect("/")


@app.route("/logout")
def logout():
    """ runs logout page and deauthenticates"""
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


# median page distingush likes and disslikes baised on the email that was clicked
@app.route("/Admin")
def admin():
    """ makes database for admin page"""
    emai_l = "noahwilliamshaffer@gmail.com"
    # EMAIL = "noahwilliamshaffer"
    con = sqlite3.connect("users.db")
    cursor = con.execute("SELECT email, id, created  FROM users")
    items = cursor.fetchall()
    # return render_template('print_items.html', items=items)
    cursor.close()
    if emai_l in Admins:
        return render_template(
            "Admin.html",
            items=items,
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
    else:
        return render_template(
            "home.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )


@app.route("/Profile", methods=["GET", "POST"])  # Add a post request
def profile():
    """ runs profile page and authenticates user"""
    return render_template(
        "Profile.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/", methods=["GET", "POST"])  # Add a post request
def home():
    """ runs home page and authenticates user"""
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/disliked", methods=["GET", "POST"])
def disliked():
    """This pulls the disliked posts."""
    if request.method == "POST":
        # getting input with name = fname in HTML form
        title = request.form["title"]
        # getting input with name = lname in HTML form
        url = request.form["url"]
        # email = requests.form.get("email")
        # name = request.form.get("name")

        # SET NAME AND EMAIL PYTHON SIDE
        big = json.dumps(session.get("user"))
        bigger = json.loads(big)
        biggest = bigger["userinfo"]
        e_mail = biggest["email"]
        name = "Working"
        fill_disliked_art(name, e_mail, title, url)
    form = AddLike()
    # ema_il = "Admin2@gmail.com"
    # t_itle = "Title"
    # ur_l = "Url"
    titles_arr = []
    urls_arr = []
    conn = get_db_connection()
    titles = conn.execute("SELECT title  FROM Art").fetchall()
    urls = conn.execute("SELECT url  FROM Art").fetchall()
    conn.close()

    titles_arr = [i[0] for i in titles]
    urls_arr = [i[0] for i in urls]
    # for row in titles:

    # makes the variables available in the html file that this route points to
    return render_template(
        "news.html",
        titles_arr=titles_arr,
        urls_arr=urls_arr,
        form=form,
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


# stores it when an article is liked maybey get rig of the
# route becase this is deals with data may be a way to streemline.
@app.route("/liked", methods=["GET", "POST"])
def liked():
    """This pulls the liked posts."""
    if request.method == "POST":
        # getting input with name = fname in HTML form
        title = request.form["title"]

        # getting input with name = lname in HTML form
        url = request.form["url"]

        big = json.dumps(session.get("user"))
        bigger = json.loads(big)
        biggest = bigger["userinfo"]
        e_mail = biggest["email"]
        name = "Working"
        fill_liked_art(name, e_mail, title, url)
    form = AddLike()
    # Email = "Admin2@gmail.com"
    # Title = "Title"
    # Url = "Url"
    titles_arr = []
    urls_arr = []
    conn = get_db_connection()
    titles = conn.execute("SELECT title  FROM Art").fetchall()
    urls = conn.execute("SELECT url  FROM Art").fetchall()
    conn.close()

    titles_arr = [i[0] for i in titles]
    urls_arr = [i[0] for i in urls]
    return render_template(
        "news.html",
        titles_arr=titles_arr,
        urls_arr=urls_arr,
        form=form,
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


# show top 10 is our news rout and site that pulls from api no longer top 10mthough
# 👆 We're continuing from the steps above. Append this to your server.py file.
@app.route("/news", methods=["GET", "POST"])
def show_top_ten():
    """This shows the top ten results."""
    form = AddLike()
    # Email = "Admin2@gmail.com"
    # Title = "Title"
    # Url = "Url"
    titles_arr = []
    urls_arr = []
    conn = get_db_connection()
    titles = conn.execute("SELECT title  FROM Art").fetchall()
    urls = conn.execute("SELECT url  FROM Art").fetchall()
    conn.close()

    titles_arr = [i[0] for i in titles]
    urls_arr = [i[0] for i in urls]
    return render_template(
        "news.html",
        titles_arr=titles_arr,
        urls_arr=urls_arr,
        form=form,
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


# In this route, you pass the tuple ('GET', 'POST') to the methods
# parameter to allow both GET and POST requests.
# GET requests are used to retrieve data from the server.
# POST requests are used to post data to a specific route.
# By default, only GET requests are allowed.
# When the user first requests the /create route using a GET request,
# a template file called create.html will be rendered.
# You will later edit this route to handle POST requests for when users fill
# and submit the web form for creating new posts.
# this is where we we pull from the database

##delete funct.
##@app.route('/create/', methods=('GET', 'POST'))
##def create():
##  return render_template('create.html')

##old function don't need most likely
##@app.route("/oldnews")

##def api():
# are we sure this is supposed to be client?
# class http.client.HTTPConnection(host, port=None, [timeout, ]source_address=None, blocksize=8192)¶
# conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")

# payload = "{}"

# HTTPConnection.request(method, url, body=None, headers={}, *, encode_chunked=False)
# try this without payload parameter
# show marlee definition for body param that we are sending the payload into
# conn.request("GET", "/v0/topstories.json?print=pretty",payload)

# Should be called after a request is sent to get the response from the server.
# res = conn.getresponse()

# Reads and returns the response body, or up to the next amt bytes.
#  data = res.read()

# print(data.decode("utf-8"))

if __name__ == "__main__":
    app.run(debug=True)
