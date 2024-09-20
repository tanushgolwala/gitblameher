import pollinations.ai as ai

def create_image(prompt: str, filename: str):
      try:
            print(prompt)
            model = ai.Image()
            image = model.generate(
                  prompt=prompt,
                  model=ai.anime,
                  noLogo=True,
                  width=512,
                  height=512,
                  seed=2323
            )
            image.save(f"image_outputs/{filename}.png")
            image.save(f"image_outputs/{filename}.png")           
            print(f"Image saved as {filename}.png")
      except Exception as e:
            print("Error:", e)
