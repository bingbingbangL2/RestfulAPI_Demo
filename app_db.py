'''
Created on Dec 8, 2016

@author: bing.xia
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import os
from inspect import getargs
# import data
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


# db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20), unique=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    price = db.Column(db.Integer, unique=False)
    publisher = db.Column(db.String(20), unique=False)
    def __init__(self, name, price, publisher):
        self.name = name
        self.price = price
        self.publisher = publisher
    def __repr__(self):
        return '<Book id:%s name:%s>' % (self.id, self.name)

def createDB():
    db.create_all()
    
def addObjInDB(obj):
    db.session.add(obj)
    db.session.commit()

def deleteDB():
    db.drop_all()
    
def deleteObj(obj):
    obj.delete()
    
def verifyAccount(username, password):
    peter = User.query.filter_by(username=username, password=password).first()
    if peter:
        return True
    return False

def getAllBookById(id):
    return Book.query.filter_by(id=id)

def getAllBooksJson():
    books = Book.query.all()
    _books = []
    for book in books:
        _book = book.__dict__
        del _book["_sa_instance_state"]
        _books.append(_book)
            
    return _books

def updateObject(obj, update):
    
    obj.update(update)

    return filter(lambda t: t["id"] == update['id'], getAllBooksJson())[0]
    
if __name__ == '__main__':
#     if os.path.exists(os.path.join(basedir, 'data.sqlite')):
#         db.drop_all()
#     createDB()
#     addObjInDB(User('user1','password1'))
#     addObjInDB(User('user2','password2'))
#     addObjInDB(User('user3','password3'))
#     addObjInDB(User('user4','password4'))
#     
#     addObjInDB(Book('Python', 20, 'Dilato'))
#     addObjInDB(Book('JAVA', 30, 'Dilato'))
#     addObjInDB(Book('C#', 20, 'Dilato'))
#     print User.query.all()
#     print Book.query.all()
    getAllBooksJson()
