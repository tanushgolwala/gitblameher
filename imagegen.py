import pollinations.ai as ai

def create_image(prompt: str, filename: str):
    print(prompt)
    model = ai.Image()
    image = model.generate(
        prompt=prompt,
        # negative...width...height...height...seed...model...nologo
    )
    image.save(filename)
    print("Image saved")