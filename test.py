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


ID = 1
con = sqlite3.connect('dislikedArticles.db')
cursor = con.execute('DELETE FROM items WHERE id IN (1)')
items = cursor.fetchall()
cursor.close()
