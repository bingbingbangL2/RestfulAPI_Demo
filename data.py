'''
Created on Dec 8, 2016

@author: bing.xia
'''

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



if __name__ == '__main__':
    pass