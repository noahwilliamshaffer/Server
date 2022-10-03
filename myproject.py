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
    app.run(debug = True
