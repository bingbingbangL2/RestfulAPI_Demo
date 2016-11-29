"""
Created on Nov 28, 2016

@author: bing.xia
"""

from flask import Flask, jsonify,abort,request

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello word"


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




@app.route("/api/v1/allapis", methods=["GET"])
def get_allapis():
    return jsonify({"apis": apis});

@app.route("/api/v1/books", methods=["GET"])
def get_allbooks():
    return jsonify({"books": books});

@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_bookbyid(book_id):
    book = filter(lambda t: t["id"] == book_id, books)
    if len(book) == 0:
        abort(404)
    return jsonify({"book": book[0]});

@app.route("/api/v1/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = filter(lambda t: t["id"] == book_id, books)
    if len(book) == 0:
        abort(404)
    books.remove(book[0])
    return jsonify({"result": "success"})

@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = filter(lambda t: t["id"] == book_id, books)
    if len(book) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'price' in request.json and type(request.json['price']) is not int:
        abort(400)
    if 'publisher' in request.json and type(request.json['publisher']) is not unicode:
        abort(400)
    
    book[0]['name'] = request.json.get('name', book[0]['name'])
    book[0]['price'] = request.json.get('price', book[0]['price'])
    book[0]['publisher'] = request.json.get('publisher', book[0]['publisher'])
    return jsonify({"book": book[0]})
    
@app.route("/api/v1/books", methods=["POST"])
def create_task():
    if not request.json or not "name" in request.json:
        abort(400)
    book = {
        "id": books[-1]["id"] + 1,
        "name": request.json["name"],
        "price": request.json["price"],
        "publisher": request.json["publisher"]
    }
    books.append(book)
    return jsonify({"book": book}), 201



if __name__ == "__main__":
    app.run(debug=True)