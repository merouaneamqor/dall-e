from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/generate_image", methods=["POST"])
def generate_image():
    # Extract the text and image from the request body
    data = request.get_json()
    text = data.get("text")
    image = data.get("image")

    # Make a request to the DALL-E 2 API
    response = requests.post("https://api.openai.com/v1/images/generations",
                             headers={
                                 "Content-Type": "application/json",
                                 "Authorization": "Bearer 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"
                             },
                             json={
                                 "model": "image-alpha-001",
                                 "prompt": text,
                                 "num_images":1,
                                 "size":"1024x1024"
                             })
    print(f"Received response from DALL-E 2 API: {response.text}")

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
