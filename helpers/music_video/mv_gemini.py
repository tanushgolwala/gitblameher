import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import re
from genius_config import load_config
from mv_imagegen import create_image_cloudflare
from download_song import get_url_and_download_song
from genius import get_song_lyrics
from generate_mv import create_music_video

def initialize_model():
    config = load_config()
    genai.configure(api_key=config['api_key'])
    return genai.GenerativeModel(config['model_name'])

def get_image_prompt(scene_info):
    match = re.search(r'Prompt:(.*)', scene_info)
    return match.group(1).strip() if match else None

def handle_safety_error(response):
    if response.candidates:
        candidate = response.candidates[0]
        if candidate.finish_reason == "SAFETY":
            print("Content generation was blocked due to safety concerns:")
            for rating in candidate.safety_ratings:
                if rating.probability != "NEGLIGIBLE":
                    print(f"- {rating.category}: {rating.probability}")
            return True
    return False

def get_scenes(lyrics, delimiter="*****", kidsMode= False):
    model = initialize_model()
    prompt = '''Given the lyrics of a song, which could be in ANY language (eg english, hindi, french, punjabi etc) - I want to convert it into a music video, which comprises of a series of cutscenes. Each cutscene HAS to tell the story of the song in a visual format, and EVERY cutsene must specifically mention the entire context of the song such that it's emotion is well and truly passed. Each scene should represent 5-7 seconds of the song. When put together, all the scenes must form a coherent story that aligns with the lyrics of the song. Do not miss out on any content, even if it is deemed explicit - some songs are like that. Keep in mind, I will use AI to generate images for the scenes based on your prompt for the scene. Have AT LEAST 45 scenes:

1. Identify the key action or event that defines the scene. If it is a hum, or something like "oh-oh-oh" etc which is repeated throughout the scene (any filler, inexplicable lyric), make sure it is duly noted - the image generated must be something that acts as a filler appropriate to the context as well.
2. List the characters present in the scene. None is okay as well.
3. Describe the setting, including:
   - Location
   - Time of day (if relevant)
   - Any important environmental details (weather, atmosphere, etc.)
   - MOST importantly, the emotion. This is crucial to convey the mood of the scene.
4. Note any significant objects or props that play a role in the scene.
5. Highlight any emotional tone or mood that's important to convey. VERY important. Make sure to use strong adjectives to describe the mood. The overall theme of the whole song should also be kept solid, not varying throughout the music video.
6. Suggest a vivid visual element that could represent the scene in a picture.
7. Using the above details provide a prompt that could be used to generate an image using an AI model, that depicts every part of the image. IF IT IS A FILLER/HUMMING SCENE, THE IMAGE MUST BE AN APPROPRIATE FILLER AS WELL. For each scene, the prompt should be detailed enough to capture the essence of the scene and provide a clear visual direction for the image generation, and also provide enough context with respect to characters, settings etc. such that there is consistency in how images are generated throughout the song. THIS IMAGE IS SUPPOSED TO BE A MUSIC VIDEO LIKE COHERENCE, NOT JUST LIKE A NORMAL NOVEL/STORY.

Format the output as follows:

Scene [Number]: [Key Action/Event]
Characters: [List of characters present]
Setting:
- Location: [Where the scene takes place]
- Time: [Time of day, if relevant]
- Details: [Important environmental elements]
- Emotion: [Emotional tone or mood of the scene]
Objects: [List of significant objects or props]
Tone: [Emotional tone or mood of the scene]
Visual Focus: [Suggestion for a key visual element]
Prompt: [Prompt for image generation]
*****

Repeat this structure for each significant scene in the book, making sure to include the string of 5 asterisks after each scene and ensuring that the breakdown captures the essence of the story and provides enough detail for creating illustrations.
MAKE SURE THE 5 ASTERISKS DELIMITER IS THERE
Here is the text:
'''

    try:
        response = model.generate_content([prompt + lyrics], safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        })
        
        if handle_safety_error(response):
            return []
        
        scenes = response.text.split(delimiter)
        return [scene.strip() for scene in scenes if scene.strip()]
    
    except Exception as e:
        print(f"Error in get_scenes: {e}")
        return []


def generate_images_and_audio_for_scenes(scenes):
    for i in range(len(scenes)):
        try:
            scene = scenes[i]
            print(scene)
            print(f"Generating image for scene {i+1}...")
            prompt = get_image_prompt(scene)
            
            print("Generating image for scene", i+1)
            if prompt:
                try:
                    create_image_cloudflare(prompt, f'music_video_scene_{i+1}')
                except:
                    print(f"Error generating image for scene {i+1}")
            else:
                print(f"Prompt not found for scene {i+1}")

        except Exception as e:
            print(f"Error in generate_images_and_audio_for_scenes: {e}. Retrying scene {i+1}...")
            i = i - 1
            continue
        

def story_to_images(story, song_name):
    scenes = get_scenes(story)
    # print(scenes)
    n = len(scenes)
    generate_images_and_audio_for_scenes(scenes)
    create_music_video(n, song_name)
    
def generate_music_video(song_name, artist):
    lyrics = get_song_lyrics(song_name, artist)
    if lyrics:
        get_url_and_download_song(song_name, artist)
        story_to_images(story=lyrics, song_name=song_name)
    else:
        print("Lyrics not found for the song")
        return

generate_music_video('a little piece of heaven', 'avenged sevenfold')

