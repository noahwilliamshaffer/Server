import pytest
import os
import tempfile
#important part of test ^
#import sqlite3
#import requests
#import http.client
#import json
#from os import environ as env
#from urllib.parse import quote_plus, urlencode
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField
#from wtforms.validators import DataRequired, Length, email, EqualTo
#from authlib.integrations.flask_client import OAuth
#from dotenv import find_dotenv, load_dotenv
#from flask import Flask, redirect, render_template, session, url_for, request



from myproject import myproject


@pytest.fixture
def client():
    db_fd, myproject.app.config['DATABASE'] = tempfile.mkstemp()
    myproject.app.config['TESTING'] = True

    with myproject.app.test_client() as client:
        with myproject.app.app_context():
            myproject.init_db()
        yield client

    os.close(db_fd)
    os.unlink(myproject.app.config['DATABASE'])
#
def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data


ID = 1
con = sqlite3.connect('dislikedArticles.db')
cursor = con.execute('DELETE FROM items WHERE id IN (1)')
items = cursor.fetchall()
cursor.close()
