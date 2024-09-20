from fastapi import FastAPI

from helpers import imagegen

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/generate-image-from-prompt")
def generate_image_from_prompt(prompt: str, filename: str):
    imagegen.create_image(prompt, filename)
    return {"status": "success", "filename": filename}