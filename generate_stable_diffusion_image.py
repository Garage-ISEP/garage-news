from PIL import Image
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

STABLE_DIFFUSION_API_KEY = os.getenv("STABLE_DIFFUSION_API_KEY")

def generate_stable_diffusion_image(prompt,lab: str):
    url = "https://stablediffusionapi.com/api/v3/text2img"
    payload = json.dumps({
      "key": STABLE_DIFFUSION_API_KEY,  # you should set this to your actual Stable Diffusion API key
      "prompt": prompt,
      "negative_prompt": None,
      "width": "1080",
      "height": "1080",
      "samples": "1",
      "num_inference_steps": "20",
      "seed": None,
      "guidance_scale": 7.5,
      "safety_checker": "yes",
      "multi_lingual": "no",
      "panorama": "no",
      "self_attention": "no",
      "upscale": "no",
      "embeddings_model": "embeddings_model_id",
      "webhook": None,
      "track_id": None
    })

    headers = {
      'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        image_url = response.json()['output'][0]

        # Save the image data to a file
        with open(f'output/bg_{lab}.png', 'wb') as f:
            f.write(requests.get(image_url).content)

        # Open the file using `Image.open`
        image = Image.open(f'output/bg_{lab}.png')
        image.save(f'output/bg_{lab}.png')
    except Exception as e:
        print("Error generating image:", e)
