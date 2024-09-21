import cv2
import os
from PIL import Image, ImageDraw, ImageFont
print("Booting Models...")
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


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

def add_text_harder(image_path, output_path,dialogue):
    base_options = python.BaseOptions(model_asset_path='blaze_face.tflite')
    options = vision.FaceDetectorOptions(base_options=base_options)
    detector = vision.FaceDetector.create_from_options(options)

    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    detection_result = detector.detect(mp_image)

    if detection_result.detections:
        main_face = max(detection_result.detections, key=lambda detection: detection.bounding_box.width * detection.bounding_box.height)
        
        bbox = main_face.bounding_box
        x = int(bbox.origin_x)
        y = int(bbox.origin_y)
        w = int(bbox.width)
        h = int(bbox.height)

        pil_img = Image.fromarray(img_rgb)

        text = dialogue
        add_text_bubble(pil_img, text, x, y - int(h * 0.5), w)

        pil_img.save(output_path)
        print(f"Processed image saved as {output_path}")
    else:
        print("No faces detected in the image.")

    detector.close()

