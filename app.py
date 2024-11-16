from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

#Initialize Flask App

load_dotenv()

app = Flask(__name__)


#Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

#test route to ensure the server is running
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the BR App!"})
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


#run the app
if __name__ == "__main__":
    app.run(debug=True)

