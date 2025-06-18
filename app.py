from flask import Flask, request, jsonify   # Flask core and utilities
import requests                             # For sending HTTP requests to Spoonacular

# Create the Flask application
app = Flask(__name__)

# Your Spoonacular API key
SPOONACULAR_API_KEY = "b8520e1af2774f3799f4c09c5d1ee5d4"

# Route to handle meal image analysis
@app.route('/analyze_meal_photo', methods=['POST'])
def analyze_meal_photo():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']

    # Send image to Spoonacular's analysis endpoint
    response = requests.post(
        f"https://api.spoonacular.com/food/images/analyze?apiKey={SPOONACULAR_API_KEY}",
        files={"file": (image_file.filename, image_file, image_file.content_type)}
    )

    # Return the result if successful
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to analyze image", "details": response.text}), 500

# ✅ Start the Flask app (only if run directly)
if __name__ == '__main__':
    app.run(debug=True)
