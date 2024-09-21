import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
from comicators.hardercomicator import add_text_harder

def add_text_bubble(image, text, x, y, face_width):
    draw = ImageDraw.Draw(image)
    font_size = int(face_width * 0.15)
    font = ImageFont.truetype("arial.ttf", font_size)

    max_text_width = int(face_width * 0.9)

    lines = []
    for line in text.split('\n'):
        wrapped_lines = wrap(line, width=30)
        lines.extend(wrapped_lines)

    text_heights = []
    max_line_width = 0
    for line in lines:
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        text_width = right - left
        text_height = bottom - top
        text_heights.append(text_height)
        max_line_width = max(max_line_width, text_width)

    bubble_padding_x = int(face_width * 0.1)
    bubble_padding_y = int(face_width * 0.05)

    bubble_width = max_line_width + 3 * bubble_padding_x
    total_text_height = sum(text_heights) + (len(lines) - 1) * bubble_padding_y
    bubble_height = total_text_height + 3 * bubble_padding_y

    ellipse_padding = int(face_width * 0.02)
    draw.ellipse([x - ellipse_padding,
                  y - bubble_height - ellipse_padding,
                  x + bubble_width + ellipse_padding,
                  y + ellipse_padding],
                 fill='white', outline='black')

    current_y = y - bubble_height + bubble_padding_y
    for i, line in enumerate(lines):
        draw.text((x + bubble_padding_x, current_y),
                  line, font=font, fill='black')
        current_y += text_heights[i] + bubble_padding_y


def face_text_adder(image_path, output_path, dialogue):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        main_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = main_face

        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        text = dialogue
        add_text_bubble(pil_img, text, x, y - int(h * 0.5), w)

        pil_img.save(output_path)
        print(f"Processed image saved as {output_path}")
    else:
        print("No faces detected in the image.... Adding Harder")
        add_text_harder(image_path, output_path, dialogue)

# n = int(input("Enter what kind of image you want to process (1.Straight Face, 2. Sideways Face): "))
# if n == 1:
#     face_text_adder("image_inputs/lincoln_speech.png", "image_outputs/lincoln_speech_text.png",
#                     "I am not bound to win,\n but I am bound to be true")
# else:
#     face_text_adder("image_inputs/sherlock.jpg",
#                     "image_outputs/sherlock_text.png", "Elementary, my dear Watson")

