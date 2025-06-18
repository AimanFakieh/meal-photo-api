# Import necessary libraries
from flask import Flask, request, jsonify   # Flask for creating the web server and handling requests/responses
import requests                             # For sending HTTP requests (to Spoonacular API)
import os                                   # To access environment variables (used for port binding)

# Create a Flask application instance
app = Flask(__name__)  # This creates the Flask app and allows you to define API routes

# Define your Spoonacular API key (keep this secret in production)
SPOONACULAR_API_KEY = "b8520e1af2774f3799f4c09c5d1ee5d4"

# ✅ HEALTH CHECK ROUTE FOR RENDER
@app.route("/")  # This defines a route for GET requests to the root URL (e.g., https://your-app.onrender.com/)
def home():
    return "Meal Photo API is running! 🚀"  # Simple confirmation message so Render knows the app is active

# ✅ API ENDPOINT: Analyze an uploaded meal photo using Spoonacular
@app.route('/analyze_meal_photo', methods=['POST'])  # This route accepts POST requests to /analyze_meal_photo
def analyze_meal_photo():
    # Check if the request contains an 'image' file
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400  # Return an error if no image is found

    # Get the uploaded image file
    image_file = request.files['image']

    # Send the image to Spoonacular's food image analysis API
    response = requests.post(
        f"https://api.spoonacular.com/food/images/analyze?apiKey={SPOONACULAR_API_KEY}",  # API endpoint with your key
        files={"file": (image_file.filename, image_file, image_file.content_type)}  # Upload the image file
    )

    # If the API request was successful, return the JSON result
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        # If the API call failed, return an error with the API's error response
        return jsonify({"error": "Failed to analyze image", "details": response.text}), 500

# ✅ RUN FLASK SERVER (only when running this file directly, not during imports)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get the port from environment (default to 5000)
    app.run(host="0.0.0.0", port=port, debug=True)  # Start the Flask server on 0.0.0.0 so Render can access it
