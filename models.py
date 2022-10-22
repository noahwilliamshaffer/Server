
from . import db
from flask_login import userMixin
from sqlaclhemy.sql import func

#we need font awesome for incons for likes

class User.(db.Model, UserMixin):
    id = db.column(db.integer, Primary_key = True)
    email = db.column(db.string(150),unique = True)
    username = db.column(db.string(150),unique = True)
    password = db.column(db.string(150))
    date_created = db.column(db.DateTime(timezone = True),defualt = func.now())

     #connects post to user
     posts = db.relationship('Post',backref = 'User', passive deletes = True)
     comments = db.relationship('Comment',backref = 'User', passive deletes = True)
     likes = db.relationship('Like',backref = 'User', passive deletes = True)

class Post (db.Model):
    id = db.column(db.integer, Primary_key = True)
    text = db.column(db.text, nullable = False)
    date_created = db.column(db.DateTime(timezone = True),defualt = func.now())
    author = db.column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"), nullable = False)

    #connects comment to post
    comments = db.relationship('Comment',backref = 'Post', passive deletes = True)
    likes = db.relationship('Like', backref = 'Post', passive deletes = True)

class Comment (db.Model):
    id = db.column(db.integer, Primary_key = True)
    text = db.column(db.string(200), nullable = False)
    date_created = db.column(db.DateTime(timezone = True),defualt = func.now())
    author = db.column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"), nullable = False)
    post_id =  db.column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"), nullable = False)

class Like(db.Model):
     id = db.column(db.integer, Primary_key = True)

    #can't hurt to add even if we don't end up using it
     date_created = db.column(db.DateTime(timezone = True),defualt = func.now())

     author = db.column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"), nullable = False)
     post_id =  db.column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"), nullable = False)
