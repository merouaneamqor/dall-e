from flask import Flask, request, jsonify, send_file
import os
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/generate_image", methods=["GET", "POST"])
def generate_image():
    if request.method == "POST":
        # Extract the text from the request body
        data = request.get_json()
        text = data.get("text")
        print(text)
    elif request.method == "GET":
        # Extract the text from the query parameters
        text = request.args.get("text")
        print(text)
    else:
        return jsonify({"error": "Invalid request method"}), 400

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

        # Make a request to download the image
        image_response = requests.get(image_url)

        # Check if the request was successful
        if image_response.status_code == 200:
            return send_file(BytesIO(image_response.content),
                             attachment_filename="generated_image.jpg",
                             mimetype="image/jpeg")
        else:
            # Return an error message
            return jsonify({"error": "Failed to download image"}), 500
    else:
        # Return an error message
        return jsonify({"error": "Failed to generate image"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
