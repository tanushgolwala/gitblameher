from moviepy.editor import *
from moviepy.config import change_settings
import os

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

def create_scene_video(scene_number):
    # Paths to the files
    image_path = f"image_outputs/scene_{scene_number}.png"
    audio_path = f"audio_outputs/scene_{scene_number}.wav"
    summary_path = f"summary_outputs/scene_{scene_number}.txt"
    
    if not all(os.path.exists(path) for path in [image_path, audio_path, summary_path]):
        print(f"Missing files for scene {scene_number}. Skipping.")
        return None
    
    image_clip = ImageClip(image_path)
    audio_clip = AudioFileClip(audio_path).set_duration(5)
    # audio_clip = AudioClip(lambda t: 0, duration=20) # Dummy audio clip
    image_clip = image_clip.set_duration(audio_clip.duration)

    # Add text overlay
    with open(summary_path, 'r') as f:
        summary = f.read()
    txt_clip = TextClip(summary, fontsize=12, color='black', bg_color='white', size=(512, 0), method='caption')
    txt_clip = txt_clip.set_duration(audio_clip.duration)
    txt_clip = txt_clip.set_position(('center', 'bottom'))
    
    # Combine the clips
    final_clip = CompositeVideoClip([image_clip, txt_clip])
    
    # Set the audio
    final_clip = final_clip.set_audio(audio_clip)
    
    # Write the final clip
    final_clip.write_videofile(f"final_scenes/scene_{scene_number}.mp4", codec='libx264', fps=24)
    
    return final_clip

def create_full_video():
    scene_number = 1
    clips = []
    
    while True:
        print(f"Creating scene {scene_number}...")
        scene_clip = create_scene_video(scene_number)
        if scene_clip is None:
            break
        clips.append(scene_clip)
        scene_number += 1
    
    if not clips:
        print("No scenes were created. Check your input files.")
        return
    
    # Concatenate all scenes
    final_video = concatenate_videoclips(clips)
    
    # Write the result to a file
    final_video.write_videofile("final_scenes/final_story.mp4", fps=24)
    
create_full_video()