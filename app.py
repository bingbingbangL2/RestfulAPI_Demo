"""
Created on Nov 28, 2016

@author: bing.xia
"""

from flask import Flask, jsonify,abort,request, make_response
from flask_httpauth import HTTPBasicAuth 
from functools import wraps
import app_db as ab
# import data
from data import apis

app = ab.app



@app.route("/")
def index():
    return "Hello world"


auth = HTTPBasicAuth()


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return ab.verifyAccount(username, password)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return unauthorized()
        return f(*args, **kwargs)
    return decorated
    

def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route("/api/v1/allapis", methods=["GET"])
@requires_auth
def get_allapis():
    return jsonify({"apis": apis});

@app.route("/api/v1/books", methods=["GET"])
@requires_auth
def get_allbooks():
    return jsonify({"books": ab.getAllBooksJson()});

@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
@requires_auth
def get_bookbyid(book_id):
    book = filter(lambda t: t["id"] == book_id, ab.getAllBooksJson())
    if len(book) == 0:
        abort(404)
    return jsonify({"book": book[0]});

@app.route("/api/v1/books/<int:book_id>", methods=["DELETE"])
@requires_auth
def delete_book(book_id):
    book = filter(lambda t: t["id"] == book_id, ab.getAllBooksJson())
    if len(book) == 0:
        abort(404)
    
    ab.deleteObj(ab.getAllBookById(book[0]['id']))
    return jsonify({"result": "success"})

@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
@requires_auth
def update_book(book_id):
    book = filter(lambda t: t["id"] == book_id, ab.getAllBooksJson())
    if len(book) == 0:
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Please send with your payload'}), 400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        return make_response(jsonify({'error': 'Type of name is not str'}), 400)
    if 'price' in request.json and type(request.json['price']) is not int:
        return make_response(jsonify({'error': 'Type of price is not int'}), 400)
    if 'publisher' in request.json and type(request.json['publisher']) is not unicode:
        return make_response(jsonify({'error': 'Type of publisher is not str'}), 400)
    
    update = {
              'id': book_id,
              'name': request.json.get('name', book[0]['name']),
              'price': request.json.get('price', book[0]['price']),
              'publisher':request.json.get('publisher', book[0]['publisher'])
              }
    
    return jsonify({"book": ab.updateObject(ab.getAllBookById(book_id),update)})
    
@app.route("/api/v1/books", methods=["POST"])
@requires_auth
def create_book():
    if not request.json or not "name" in request.json:
        return make_response(jsonify({'error': 'Please send with your payload, or missed field name'}), 400)
    _publisher = "no publisher"
    _price=0
    if 'price' in request.json:
        if type(request.json['price']) is not int:
            return make_response(jsonify({'error': 'Type of price is not int'}), 400)
        else:
            _price = request.json["price"]
    if 'publisher' in request.json:
        if type(request.json['publisher']) is not unicode:
            return make_response(jsonify({'error': 'Type of publisher is not str'}), 400)
        else:
            _publisher = request.json["publisher"]

    book = ab.Book(request.json["name"], _price, _publisher)
    ab.addObjInDB(book)
    return jsonify({"book": (filter(lambda t: t["id"] == book.id, ab.getAllBooksJson()))[0]}), 201



if __name__ == "__main__":
    app.run(debug=True)