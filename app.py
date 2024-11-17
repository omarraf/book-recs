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
    ''' 
    This function handles user requests to get recommendations based on book title, author, or topic.
    It queries Google Books API and returns formatted recommendations
    '''
    # get query from user request
    query = request.args.get("q")

    if not query or len(query.strip()) <= 3: #validate query, maybe implement more advanced version to handle queries
        return jsonify({"error": "Please enter a valid book, topic or author (At least 3 characters long)"}), 400
    
    #load the api key and build the url
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}&maxResults=10"
    #This URL queries the Google Books API with:
    # - 'q={query}': Search term provided by user
    # - 'key={api_key}': api key required for auth
    # - 'maxResults=10': limits the number of results to 10, may change later

    #send a GET response to the API
    response = requests.get(api_url) #uses request library to fetch data from the API
    # response now contains HTTP response from API, which includes data and status code

    if response.status_code == 200:
        data = response.json()
        if "items" not in data: #check if api returned any books
            return jsonify({"error": "No results found, please check for spelling or try a different query"}), 404
        
        recommendations = [] #initialize list to format books
        for item in data.get("items",[]):
            volume_info = item.get("volumeInfo", {})
            title = volume_info.get("title")

            if not title:
                continue

            recommendations.append({
                "title": title,
                "author": volume_info.get("authors", []),
                "description": volume_info.get("description", "No description available :()"),
                "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail", "No image available"),
            })
        #convert the list to json and send it as a response
        return jsonify(recommendations)
    else:
        return jsonify({"error": "Failed to fetch book recommendations, please try again later."})


#run the app
if __name__ == "__main__":
    app.run(debug=True)

