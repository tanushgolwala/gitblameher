import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import dlib

def add_text_bubble(image, text, x, y, face_width):
    draw = ImageDraw.Draw(image)
    font_size = int(face_width * 0.15)
    font = ImageFont.truetype("arial.ttf", font_size)
    
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_width = right - left
    text_height = bottom - top
    
    bubble_padding_x = int(face_width * 0.1)
    bubble_padding_y = int(face_width * 0.05)
    bubble_width = text_width + 2 * bubble_padding_x
    bubble_height = text_height + 2 * bubble_padding_y
    
    ellipse_padding = int(face_width * 0.02)
    draw.ellipse([x - ellipse_padding, 
                  y - bubble_height - ellipse_padding, 
                  x + bubble_width + ellipse_padding, 
                  y + ellipse_padding], 
                 fill='white', outline='black')
    
    draw.text((x + bubble_padding_x, y - bubble_height + bubble_padding_y), text, font=font, fill='black')

def detect_main_face_and_add_text(image_path, output_path):
    detector = dlib.get_frontal_face_detector()

    img = cv2.imread(image_path)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faces = detector(rgb_img)

    if len(faces) > 0:
        main_face = max(faces, key=lambda rect: rect.width() * rect.height())
        
        x, y = main_face.left(), main_face.top()
        w, h = main_face.width(), main_face.height()

        pil_img = Image.fromarray(rgb_img)

        text = "Main Character"
        add_text_bubble(pil_img, text, x, y - int(h * 0.5), w)

        pil_img.save(output_path)
        print(f"Processed image saved as {output_path}")
    else:
        print("No faces detected in the image.")

input_image = "image_outputs/tmst.png"
output_image = "image_outputs/speeched.jpg"
detect_main_face_and_add_text(input_image, output_image)