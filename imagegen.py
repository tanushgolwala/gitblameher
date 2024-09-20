import pollinations.ai as ai

def create_image(prompt: str, filename: str):
    model = ai.Image()
    image = model.generate(
        prompt=prompt,
        # negative...width...height...height...seed...model...nologo
    )
    image.save(filename)
    print(image)