import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests

from flask_sqlalchemy import SQLAlchemy

#load env variables from .env
load_dotenv()

#Initialize Flask App
app = Flask(__name__)

#Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Configure SQLite database
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"  # SQLite file named books.db
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False          # Turn off modification tracking for performance
# db = SQLAlchemy(app)                                          # Initialize the SQLAlchemy object
 

# class FavoriteBook(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable = False)
#     author = db.Column(db.String(100))
#     description = db.Column(db.Text)

#     def __repr__(self):
#         return f"<FavoriteBook {self.title}>"




#test route to ensure the server is running
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the BR App!"})

#route to search for books
@app.route("/search", methods=["GET"])
def search_books():
    #getting search query from request
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query paramater 'q' is required"}), 400
    
    #build google books api key
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    #load the url
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"

    response = requests.get(api_url)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data"})

@app.route("/recommend", methods=["GET"])
def recommend_books():
    #getting query
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Please enter a valid book, topic or author"}), 400
    
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}&maxResults=10"

    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if "items" not in data:
            return jsonify({"error": "No results found, please check for spelling or try a different query"}), 404







# @app.route("/favorites", methods=["POST"])
# def add_favorite():
#     #Get the data from the request body
#     data = request.json
#     if not data or not data.get("title"):
#         return jsonify({"error": "title is required"}), 400
    
#     favorite = FavoriteBook (
#         title = data["title"],
#         author = data.get("author"),
#         description = data.get("description"),
#     )
#     #add to database and commit transaction
#     db.session.add(favorite)
#     db.session.commit()

#     return jsonify({"message": "Book added to favorites"})

# @app.route("/favorites", methods=["GET"])
# def get_favorites():
#     #query all favorite books from the database
#     favorites = FavoriteBook.query.all()

#     #converts the results to a list of dictionaries 
#     results = [
#         {
#             "id" : book.id,
#             "title" : book.title,
#             "author" : book.author,
#             "description" : book.description,
#         }
#         for book in favorites
#     ]
#     return jsonify(results)

# @app.route("/favorites/<id>",methods=["DELETE"])
# def delete_favorite(id):
#     book_to_delete = FavoriteBook.query.get(id)
#     if not book_to_delete:
#         return jsonify({"error": "Book not found in favorites."}), 404
#     else:
#         db.session.delete(book_to_delete)
#         db.session.commit()
#         return jsonify({"message": "Book successfully deleted from favorites"})

# with app.app_context():
#     db.create_all()

#run the app
if __name__ == "__main__":
    app.run(debug=True)

