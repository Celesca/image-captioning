import os
import ollama

folder_path = 'input_image'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        print(f'Processing file: {file_path}')