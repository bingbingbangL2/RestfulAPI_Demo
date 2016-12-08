"""
Created on Nov 28, 2016

@author: bing.xia
"""

from flask import Flask, jsonify,abort,request, make_response
from flask_httpauth import HTTPBasicAuth 
from functools import wraps
app = Flask(__name__)


@app.route("/")
def index():
    return "Hello world"

apis=[
       {
       "GET: All Books":"/api/v1/books, get all books"
       },
      {
       "GET: Get Book by id":'/api/v1/books/{id}, by book id'
       },
      {
       "DELETE: Book":"/api/v1/books/{id}, delete book by id"
       },
      {
       "POST: Book":'/api/v1/books, payload: name: str, required; price: int  optional; publisher str optional'
       },
      {
       "PUT: Book":'/api/v1/books/{id}, payload: name : str optional; price: int  optional; publisher str optional'
       }
      ]

books = [
         {
          "id":1,
          "name":"Python",
          "price":20,
          "publisher":"Dilato"
          },
         {
          "id":2,
          "name":"C Sharp",
          "price":30,
          "publisher":"Dilato"
          },
         {
          "id":3,
          "name":"Java",
          "price":30,
          "publisher":"Dilato"
          },
         ]

accounts = {
           "user1":"password1",
           "user2":"password2",
           "user3":"password3",
           "user4":"password4",
           }

auth = HTTPBasicAuth()


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    if username in accounts.keys() and password == accounts[username]: 
        return True
    return False


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
    return jsonify({"books": books});

@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
@requires_auth
def get_bookbyid(book_id):
    book = filter(lambda t: t["id"] == book_id, books)
    if len(book) == 0:
        abort(404)
    return jsonify({"book": book[0]});

@app.route("/api/v1/books/<int:book_id>", methods=["DELETE"])
@requires_auth
def delete_book(book_id):
    book = filter(lambda t: t["id"] == book_id, books)
    if len(book) == 0:
        abort(404)
    books.remove(book[0])
    return jsonify({"result": "success"})

@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
@requires_auth
def update_book(book_id):
    book = filter(lambda t: t["id"] == book_id, books)
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
    
    book[0]['name'] = request.json.get('name', book[0]['name'])
    book[0]['price'] = request.json.get('price', book[0]['price'])
    book[0]['publisher'] = request.json.get('publisher', book[0]['publisher'])
    return jsonify({"book": book[0]})
    
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
    book = {
        "id": books[-1]["id"] + 1,
        "name": request.json["name"],
        "price": _price,
        "publisher": _publisher
    }
    books.append(book)
    return jsonify({"book": book}), 201



if __name__ == "__main__":
    app.run(debug=True)