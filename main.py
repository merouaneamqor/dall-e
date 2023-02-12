from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route("/generate_image", methods=["POST"])
def generate_image():
    # Extract the text and image from the request body
    data = request.get_json()
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
                                 "num_images":1,
                             })
    print(response.json())

    # Check if the request was successful
    if response.status_code == 200:
        image_url = response.json().get("data")[0].get("url")
        # Return the generated image URL
        return jsonify({"image_url": image_url})
    else:
        # Return an error message
        return jsonify({"error": "Failed to generate image"}), 500

if __name__ == "__main__":
    app.run()
