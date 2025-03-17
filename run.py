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

# Define explanation styles
EXPLANATION_STYLES = {
    "ELI5": "Explain this as if you were talking to a 5-year-old, using simple words and relatable examples.",
    "Student": "Explain this to a high school or university student, providing more details and examples, but keeping it digestible.",
    "Grandparent": "Explain this as if you were explaining it to an elderly person who is curious but unfamiliar with modern concepts."
}

@app.route('/explain', methods=['POST'])
def explain():
    data = request.json
    query = data.get("query", "")
    category = data.get("category", "")
    style = data.get("style", "")

    if not query or not category or not style:
        return jsonify({"error": "Missing query, category, or style"}), 400

    style_prompt = EXPLANATION_STYLES.get(style, "Explain this topic clearly and concisely.")

    try:
        # Generate response using Gemini with explicit paragraph instructions
        response = model.generate_content(
            f"{style_prompt} The topic is {query} in the field of {category}. " +
            "Format your explanation with multiple paragraphs for better readability. " +
            "Use 3-4 sentences per paragraph maximum, and separate key concepts into different paragraphs."
        )
        
        # Extract and format the explanation
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
