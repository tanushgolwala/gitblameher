import requests
import dotenv
import os

dotenv.load_dotenv()
huggingface_api = os.getenv("HUGGINGFACE_KEY")

API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
headers = {"Authorization": "Bearer " + huggingface_api}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

def generate_music(input_prompt: str, filename: str):
	error = False
 
	audio_bytes = query({
		"inputs": input_prompt,
	})

	if audio_bytes == b'Internal Server Error':
		print("Internal Server Error")
		audio_bytes = b''
		error = True

	with open(f"audio_outputs/{filename}.wav", "wb") as f:
		f.write(audio_bytes)

	print(f"Audio file saved as {filename}.wav")
	return error, filename