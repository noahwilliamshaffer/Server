# 📁 API.py -----
#implementing the API in flask

from flask import flask, request

//Requesting from a website
@app.route(...) 
def login():
    username = request.args.get('username')
    password = request.args.get('password')
