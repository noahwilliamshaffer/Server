# 📁 API.py -----
#implementing the API in flask
{% extends "base.html" %}
{% block title %} Login{%EndOfBlock}

from flask import flask, request

//Requesting from a website
@app.route(...) 
def login():
    username = request.args.get('username')
    password = request.args.get('password')
