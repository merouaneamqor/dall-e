from flask import Flask, request, jsonify, send_file
import os
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/generate_image", methods=["GET", "POST"])
def generate_image():
    # Check if the request's Content-Type header is set to application/json
    if request.headers.get("Content-Type") == "application/json":
        data = request.get_json()
    else:
        # Try to convert the request data to JSON
        try:
            data = request.get_json(force=True)
        except:
            # Return an error message if the conversion fails
            return jsonify({"error": "Content-Type must be set to application/json"}), 400
    text = data.get("text")

    # Get the API key from the Heroku environment
    api_key = os.environ.get("DALL_E_API_KEY")

    # Make a request to the DALL-E 2 API
    response = requests.post("https://api.openai.com/v1/images/generations",
                             headers={
                                 "Content-Type": "application/json",
                                 "Authorization": f"Bearer {api_key}"
                             },
                             json={
                                 "model": "image-alpha-001",
                                 "prompt": text,
                                 "num_images": 1,
                             })

    # Check if the request was successful
    if response.status_code == 200:
        image_url = response.json().get("data")[0].get("url")
        # Return the generated image URL
        return jsonify({"image_url": image_url})
    else:
        # Return an error message
        return jsonify({"error": "Failed to generate image"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
