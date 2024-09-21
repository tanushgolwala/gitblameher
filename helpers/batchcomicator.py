from comicators.comicator import face_text_adder

import os

def batchcomicator(image_dir, dialogues, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(valid_extensions)]

    if len(image_files) != len(dialogues):
        print("Error: The number of images and dialogues must match.")
        return

    for i, (image_file, dialogue) in enumerate(zip(image_files, dialogues)):
        image_path = os.path.join(image_dir, image_file)
        output_path = os.path.join(output_dir, f"output_image_{i + 1}.jpg")
        print(f"Processing image: {image_path} with dialogue: {dialogue}")
     
        face_text_adder(image_path, output_path, dialogue)

    print(f"Processed {len(image_files)} images successfully.")

