import pollinations.ai as ai

# Version 1
model: ai.Image = ai.Image()
image: ai.ImageObject = model.generate(
      prompt="A cat playing with a ball",
      # negative...width...height...height...seed...model...nologo
)
image.save("cat_playing_with_ball.png")
print(image)