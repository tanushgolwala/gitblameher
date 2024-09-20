from fastapi import FastAPI, File, UploadFile
from helpers import imagegen
from helpers.inputter import Inputter
from typing import Annotated
from helpers.utils import get_flag_based_on_extension

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/generate-image-from-prompt")
def generate_image_from_prompt(prompt: str, filename: str):
    imagegen.create_image(prompt, filename)
    return {"status": "success", "filename": filename}

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    inputter = Inputter(file.file, get_flag_based_on_extension(file.filename))
    extracted_text = inputter.read()
    return {"extracted_text": extracted_text}
