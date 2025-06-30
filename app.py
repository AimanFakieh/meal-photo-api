# ✅ Import necessary libraries
from flask import Flask, request, jsonify       # Flask for API
import requests                                 # For calling Spoonacular
import os                                       # For environment variables
import traceback                                # For detailed error logging

# ✅ Initialize the Flask app
app = Flask(__name__)

# ✅ Your Spoonacular API Key (loaded securely from environment variables)
SPOONACULAR_API_KEY = os.environ.get("SPOONACULAR_API_KEY")

# ✅ Health check route
@app.route("/")
def home():
    return "Meal Photo API is running! 🚀"

# ✅ Main route to analyze meal image
@app.route('/analyze_meal_photo', methods=['POST'])
def analyze_meal_photo():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image_file = request.files['image']

        # Save image temporarily (Spoonacular API sometimes fails with in-memory streams)
        temp_path = f"/tmp/{image_file.filename}"
        image_file.save(temp_path)

        # Open it in binary mode
        with open(temp_path, 'rb') as f:
            files = {'file': (image_file.filename, f, image_file.content_type)}
            headers = {
                "Content-Type": "multipart/form-data"
            }
            response = requests.post(
                f"https://api.spoonacular.com/food/images/analyze?apiKey={SPOONACULAR_API_KEY}",
                files=files,
                headers=headers
            )

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            print("❌ Spoonacular error:", response.status_code, response.text)
            return jsonify({
                "error": "Failed to analyze image",
                "details": response.text
            }), 500

    except Exception as e:
        print("⚠️ Exception occurred:", e)
        print(traceback.format_exc())
        return jsonify({
            "error": "Server crashed",
            "message": str(e)
        }), 500

# ✅ Optional: Run server locally (not used in Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
