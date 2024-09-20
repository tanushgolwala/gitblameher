import pollinations.ai as ai

def create_image(prompt: str, filename: str, summary:str=""):
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
            #create txt file in image_outputs folder with summary
            with open(f"summary_outputs/{filename}.txt", "w") as text_file:
                  text_file.write(summary)
            print(f"Image saved as {filename}.png")

      except Exception as e:
            print("Error:", e)
