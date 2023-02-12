import requests
import json

url = "http://127.0.0.1:5000/generate_image"

data = {
    "text": "A group of dogs playing in a park",
    "image": "https://cf-s3.petcoach.co/uploads/noslidesarticleimages/e4fc25bfc8bd5b99914d911d89612407.jpg"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    image_url = response.json().get("image_url")
    print(f"Generated image URL: {image_url}")
else:
    print("Failed to generate image")
