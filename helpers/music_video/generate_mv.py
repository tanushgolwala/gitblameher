from moviepy.editor import *
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

def create_scene_video(scene_number, len_per_clip):
    # Paths to the files
    image_path = f"image_outputs/music_video_scene_{scene_number}.png"
    
    if not all(os.path.exists(path) for path in [image_path]):
        print(f"Missing files for scene {scene_number}. Skipping.")
        return None
    
    image_clip = ImageClip(image_path)
    image_clip = image_clip.set_duration(len_per_clip)
    
    image_clip.write_videofile(f"mv_songs/music_video_scene_{scene_number}.mp4", codec='libx264', fps=24)
    
    return image_clip

def create_music_video(n, songname):
    scene_number = 1
    clips = []
    
    audio_path = f"mv_songs/{songname}.mp3"
    if not os.path.exists(audio_path):
        print(f"Missing audio file {audio_path}. Exiting.")
        return
    
    audio_clip = AudioFileClip(audio_path)
    len_per_clip = audio_clip.duration // n
    
    while True:
        print(f"Creating scene {scene_number}...")
        scene_clip = create_scene_video(scene_number, len_per_clip)
        if scene_clip is None:
            break
        clips.append(scene_clip)
        scene_number += 1
    
    if not clips:
        print("No scenes were created. Check your input files.")
        return
    
    # Concatenate all scenes
    final_video = concatenate_videoclips(clips)
    
    # Add the audio
    final_video = final_video.set_audio(audio_clip)
    
    # Write the result to a file
    final_video.write_videofile(f"mv_songs/{songname}_music_video.mp4", fps=24)
    
    for clip in clips:
        os.remove(clip.filename)
    
# create_music_video(15, "aaoge tum kabhi")
