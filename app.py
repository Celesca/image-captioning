import os
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import ollama

os.environ["OPENAI_API_KEY"] = os.getenv("GPT_TOKEN")
client = OpenAI()

API_KEY = os.getenv("GPT_TOKEN")

def generate_prompts_from_image(file_name):
    res = ollama.chat(
	model="llava",
	messages=[
		{
			'role': 'user',
			'content': 'Describe this image in 200 words or less:',
			'images': [file_name]
		}
	]
    )

    return res['message']['content'] 

def generate_images_from_prompts(api_key, prompts, original_name, save_path):
    
    print("Generating images from prompts...")

    print(f"Generating image... {prompts}")

    # model for ChatGPT plus is "dall-e-3"
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompts,
        quality="standard",
        n=1,
    )
    image_url = response["data"][0]["url"]
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    image_filename = os.path.join(save_path, f"{original_name}.png")
    image.save(image_filename)
    print(f"Image saved to {image_filename}")

folder_path = 'input_image'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        print(f'Processing file: {file_path}')

        prompts = generate_prompts_from_image(file_path)

        generate_images_from_prompts(API_KEY, prompts, filename, 'output_image')

print("Done!")