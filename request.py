import requests
import json

url = "https://images-endpoint.herokuapp.com/generate_image"

data = {
    "text": "4K studio photography set of high detail irregular marble stones with gold lines stacked in impossible balance, perfect composition, cinematic light photo studio, beige color scheme, indirect lighting, 8k, elegant and luxury style",
}
response = requests.get(url, json=data)

if response.status_code == 200:
    image_url = response.json().get("image_url")
    print(f"Generated image URL: {image_url}")
else:
    print("Failed to generate image")
