# ✅ Import necessary libraries
from flask import Flask, request, jsonify       # Flask for API
import requests                                 # For calling Spoonacular
import os                                       # For environment variables
import traceback                                # For detailed error logging

# ✅ Initialize the Flask app
app = Flask(__name__)

# ✅ Your Spoonacular API Key (keep this private!)
SPOONACULAR_API_KEY = "b8520e1af2774f3799f4c09c5d1ee5d4"  # Replace this if you rotate the key

# ✅ Health check route (to test if API is running)
@app.route("/")
def home():
    return "Meal Photo API is running! 🚀"

# ✅ Main route to analyze meal image
@app.route('/analyze_meal_photo', methods=['POST'])
def analyze_meal_photo():
    try:
        # 🔍 Check if image was sent
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        # 📸 Get uploaded image file
        image_file = request.files['image']

        # 🧠 Send image to Spoonacular API
        response = requests.post(
            f"https://api.spoonacular.com/food/images/analyze?apiKey={SPOONACULAR_API_KEY}",
            files={"file": (image_file.filename, image_file, image_file.content_type)}
        )

        # ✅ If successful, return Spoonacular's response
        if response.status_code == 200:
            return jsonify(response.json())

        # ❌ Log Spoonacular API error
        print("❌ Spoonacular error:", response.status_code, response.text)
        return jsonify({
            "error": "Failed to analyze image",
            "details": response.text
        }), 500

    except Exception as e:
        # 🧯 Catch internal server errors
        print("⚠️ Exception occurred:", e)
        print(traceback.format_exc())
        return jsonify({
            "error": "Server crashed",
            "message": str(e)
        }), 500

# ✅ Run the server locally (optional, Render doesn’t use this)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
