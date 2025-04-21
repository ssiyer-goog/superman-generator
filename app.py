from flask import Flask, request, jsonify, send_from_directory
from diffusers import StableDiffusionPipeline
import torch
import os

app = Flask(__name__, static_folder='static')

# Set the path to save generated images
output_path = "static/images"

# Function to load or download the model
def load_model():
    try:
        # Try to load the model from the local cache
        pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            torch_dtype=torch.float16,
            local_files_only=True,
        )
        print("Model loaded from local cache.")
    except OSError:
        # If the model is not found locally, download it
        print("Model not found locally. Downloading...")
        pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            torch_dtype=torch.float16,
        )
    return pipe.to("cuda")

pipe = load_model()

@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data['prompt']

        # Generate the image
        image = pipe(prompt).images[0]

        # Create the output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        # Save the image
        image_name = f"{hash(prompt)}.png"
        image_path = os.path.join(output_path, image_name)
        image.save(image_path)

        return jsonify({'image_url': f'/{image_path}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)