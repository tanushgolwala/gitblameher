import pollinations.ai as ai

def create_image(prompt: str, filename: str, summary:str=""):
      try:
            print(prompt)
            model = ai.Image()
            image = model.generate(
                  prompt=prompt,
                  model=ai.anime,
                  nologo=True,
                  width=1024,
                  height=1024,
                  seed=10,
            )
            image.save(f"image_outputs/{filename}.png")
            #create txt file in image_outputs folder with summary
            with open(f"summary_outputs/{filename}.txt", "w") as text_file:
                  text_file.write(summary)
            print(f"Image saved as {filename}.png")

      except Exception as e:
            print("Error:", e)


import requests
import dotenv
import os

dotenv.load_dotenv()

def create_image_cloudflare(prompt: str, filename: str, summary:str=""):
      CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
      CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
      url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0"
      headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json"
      }
      payload = {
            "prompt": prompt,
            "height": 720,
            "width": 1280,
      }
      response = requests.post(url, headers=headers, json=payload)
      if response.status_code == 200:
            # Save the image as a PNG file
            with open(f"image_outputs/{filename}.png", "wb") as f:
                  f.write(response.content)
            print("Image saved as output_image.png")
            with open(f"summary_outputs/{filename}.txt", "w") as text_file:
                  text_file.write(summary)

      else:
            print(f"Request failed with status code {response.status_code}: {response.text}")


create_image_cloudflare("A beautiful sunset over the ocean with a lighthouse in the distance", "sunset_lighthouse", "A serene scene of a lighthouse overlooking the ocean at sunset.")