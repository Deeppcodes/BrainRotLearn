import os
import google.generativeai as genai
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allows cross-origin requests

# Load API key for Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from the .env file")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Select the model
model = genai.GenerativeModel("gemini-2.0-flash")

# Backend route for explanation using Gemini
@app.route('/explain', methods=['POST'])
def explain():
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Generate response using Gemini
        response = model.generate_content(
            f"Please explain the following topic simply and concisely but with proper explanation, as if you were explaining it to a 5-year-old: {query}. Format your response with clear paragraph breaks every 2-3 sentences for readability."
        )
        
        # Extract and format the explanation with proper paragraphs
        explanation = response.text
        
        return jsonify({"explanation": explanation})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to serve the frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(os.path.join(app.root_path, ''), 'index.html')


# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
