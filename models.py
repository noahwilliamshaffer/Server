
from . import db
from flask_login import userMixin
from sqlaclhemy.sql import func


class User.(db.Model, UserMixin){
    id = db.column(db.integer, Primary_key = true)
    email = db.column(db.string(150),unique = true)
    username = db.column(db.string(150),unique = true)
    password = db.column(db.string(150))
    date_created = db.column(db.DateTime(timezone = true),defualt = func.now())

     #this is where we dfine our like model
     posts = db.relationship('post',backref = 'user', passive deletes = True unique = true)
}


