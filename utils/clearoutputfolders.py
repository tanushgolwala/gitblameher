import os
import shutil

def clear_output_folders():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    for folder in ['audio_outputs', 'image_outputs', 'summary_outputs']:
        folder_path = os.path.join(current_dir, folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path)


def copy_to_frontend():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    frontend_public_path = os.path.join(current_dir, '../frontend/public')

    for folder in ['../audio_outputs', '../image_outputs', '../summary_outputs']:
        source_folder = os.path.join(current_dir, folder)
        folder = folder.replace('../', '')
        destination_folder = os.path.join(frontend_public_path, folder)
        print(destination_folder)

        if os.path.exists(destination_folder):
            shutil.rmtree(destination_folder)
        
        shutil.copytree(source_folder, destination_folder)


# Clear and copy folders
clear_output_folders()
