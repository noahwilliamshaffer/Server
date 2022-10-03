from flask import Flask, render_template 
# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
#importing libraries that our application needs
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

#Loading our env file
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# @app.route('/')
# def welcome():
#     return "This is the home page of Flask Application"
 
@app.route('/')
def signup():
	return render_template('signup.html')
@app.route('/Login.html')
def login():
	return render_teplate('Login.html') 
if __name__=='__main__':
    app.run(debug = True)

#authorize OAuth app 
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

#adding our login route to redirect user to autho
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

#Redirecting the user to the mainpage of our app
#this will be news page
#This will also save the session for the user so they don't have to log in again
@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

#This route signs the user out of the application
#we will redirect user to logout screen
#Clears the user session in the app
#prepares them to be redirected to home route
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

#The home route either
#renders a users authenticated details
#Or allows users to sign in
@app.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4)
