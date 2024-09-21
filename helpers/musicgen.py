import requests
import dotenv
import os
import librosa
import soundfile as sf
from torch import ge

dotenv.load_dotenv()
huggingface_api = os.getenv("HUGGINGFACE_KEY")

API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
headers = {"Authorization": "Bearer " + huggingface_api}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

def generate_music_usingAPI(input_prompt: str, filename: str):

	error = False
 
	audio_bytes = query({
		"inputs": input_prompt,
	})

	if audio_bytes == b'Internal Server Error':
		print("Internal Server Error")
		audio_bytes = b''
		error = True
  
	print(audio_bytes)

	with open (f"audio_outputs/{filename}.wav", "wb") as f:
		f.write(audio_bytes)
		#preserve metadata
	f.close()
 
	#open using librosa, and write to a new wav
	y, sr = librosa.load(f"audio_outputs/{filename}.wav", duration=10)
	sf.write(f"audio_outputs/{filename}.wav", y, sr)	

	print(f"Audio file saved as {filename}.wav")
	return error, filename


from transformers import pipeline
import torch
import scipy

# Check if CUDA is available and use GPU (device=0), otherwise fall back to CPU (device=-1)
device = 0 if torch.cuda.is_available() else -1

# Initialize the pipeline with the device parameter (GPU if available)
synthesiser = pipeline("text-to-audio", "facebook/musicgen-small", device=device)

print("AUDIO GENERATION PIPELINE INITIALIZED")


def generate_music(prompt, filename, tokens):
    #600 tokens is roughly 10 seconds
    music = synthesiser(
        prompt, 
        forward_params={"do_sample": True, "max_new_tokens": tokens}  # Adjust this to tune the length
    )
    scipy.io.wavfile.write(filename, rate=music["sampling_rate"], data=music["audio"])
    return filename
