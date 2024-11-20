import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import random

from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

CORS(app)

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
        print(response.status_code)
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data"})
    

@app.route("/recommend", methods=["GET"])
def recommend_books():
    query = request.args.get("q")
    if not query or len(query.strip()) < 3:
        return jsonify({"error": "Please provide a valid book name (at least 3 characters)."}), 400

    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}&maxResults=20"  # Fetch more results
    response = requests.get(api_url)

    if response.status_code != 200 or "items" not in response.json():
        return jsonify({"error": "Failed to retrieve book. Please check the spelling and try again."}), 404

    # Extract book data
    data = response.json()
    recommendations = []
    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})
        recommendations.append({
            "title": volume_info.get("title", "No title available"),
            "author": volume_info.get("authors", []),
            "description": volume_info.get("description", "No description available"),
            "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail", "No image available"),
        })

    # Shuffle recommendations and return a random subset (e.g., 5 books)
    shuffled_recs = random.sample(recommendations, k=min(len(recommendations), 5))
    return jsonify(shuffled_recs)







#run the app
if __name__ == "__main__":
    app.run(debug=True)

