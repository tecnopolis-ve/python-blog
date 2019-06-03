# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import time, os, hashlib
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime, timedelta
from flask import Flask, abort, request, jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tzlocal import *
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '5BA827213F65646C1964C3B593FD6'
app.debug = True

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

####CLASE USUARIO

class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    username = db.Column(db.String(32), unique=True)
    pw_hash = db.Column(db.String())
    created = db.Column(db.DateTime(get_localzone()), default=datetime.now)
    updated = db.Column(db.DateTime(get_localzone()), onupdate=datetime.now)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    def __unicode__(self):
        return '%s' % self.name

    def __repr__(self):
        return '<%s#%s>' % (self.__class__.__name__, self.id)

    @staticmethod #decorador
    def verify_auth_token(token):
        s = Serializer(app.secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user

####CLASE BLOG

class Blog(db.Model):

    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime(get_localzone()), default=datetime.now)
    updated = db.Column(db.DateTime(get_localzone()), onupdate=datetime.now)

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_title(self, title):
        self.title = title

    def set_body(self, body):
        self.body = body

    def __unicode__(self):
        return '%s' % self.name

    def __repr__(self):
        return '<%s#%s>' % (self.__class__.__name__, self.id)

@app.before_request
def before_request():

    """Will be executed before each request."""
    # g.user = current_user
    g.current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

@app.context_processor
def inject_user():
    return dict(current_time=g.current_time)

if __name__ == "__main__":
    app.run(debug=app.debug, host='0.0.0.0', port=5000)
