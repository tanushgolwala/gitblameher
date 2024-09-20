import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

audio_bytes = query({
	"inputs": "epic sad morose music for a funeral scene",
})

print(audio_bytes)

# Save as wav
with open("audio_outputs/sadge.wav", "wb") as f:
    f.write(audio_bytes)

print("Audio file saved as output.wav")
