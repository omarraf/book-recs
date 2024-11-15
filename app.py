from flask import Flask, request, jsonify
from flask_cors import CORS

#Initialize Flask App
app = Flask(__name__)


#Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

#test route to ensure the server is running
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Book Recommendation App!"})

#run the app
if __name__ == "__main__":
    app.run(debug=True)
    
