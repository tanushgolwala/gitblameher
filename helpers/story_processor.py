import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import re
from config import load_config
from imagegen import create_image
import musicgen

def initialize_model():
    config = load_config()
    genai.configure(api_key=config['api_key'])
    return genai.GenerativeModel(config['model_name'])

def get_image_prompt(scene_info):
    match = re.search(r'\*\*Prompt:\*\*(.*)', scene_info)
    return match.group(1).strip() if match else None

def get_summary(scene_info):
    match = re.search(r'\*\*Summary:\*\*(.*?)\*\*Characters:', scene_info, re.DOTALL)
    print("SUMMARY:", match.group(1).strip() if match else None)
    return match.group(1).strip() if match else None

def get_audio_prompt(scene_info):
    match = re.search(r'\*\*Audio:\*\*(.*?)\*\*Visual', scene_info, re.DOTALL)
    return match.group(1).strip() if match else None

def generate_audio(audio_prompt, scene_index):
    return musicgen.generate_music(audio_prompt, f'scene_{scene_index+1}')

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

def get_scenes(story, delimiter="*****", kidsMode= False):
    model = initialize_model()
    prompt = '''Given a text-based story, break it down into distinct scenes suitable for a picture book adaptation. For each scene:

1. Identify the key action or event that defines the scene.
2. Provide a summary of what happens in the scene (2-3 sentences), this is going to be the caption in the picture book so make sure to not miss out on any details; all the summaries together should be able to form the continuous story.
3. List the characters present in the scene.
4. Describe the setting, including:
   - Location
   - Time of day (if relevant)
   - Any important environmental details (weather, atmosphere, etc.)
5. Note any significant objects or props that play a role in the scene.
6. Highlight any emotional tone or mood that's important to convey.
7. Suggest a background audio prompt for an AI background music generator that could enhance the scene. Do make sure EXTREME descriptive words are used (for example "epic" for an intense scene, "comical" for funny scenes etc.) and do mention "background music" in the prompt.
8. Suggest a vivid visual element that could represent the scene in a picture.
9. Using the above details provide a prompt that could be used to generate an image using an AI model, that depicts every part of the image. For each scene, the prompt should be detailed enough to capture the essence of the scene and provide a clear visual direction for the image generation, and also provide enough context with respect to characters, settings etc. such that there is consistency in how images are generated throughout the book.

Format the output as follows:

Scene [Number]: [Key Action/Event]
Summary: [Text shown on the panel of the picture book with this image]
Characters: [List of characters present]
Setting:
- Location: [Where the scene takes place]
- Time: [Time of day, if relevant]
- Details: [Important environmental elements]
Objects: [List of significant objects or props]
Tone: [Emotional tone or mood of the scene]
Audio: [Suggestion for background audio]
Visual Focus: [Suggestion for a key visual element]
Prompt: [Prompt for image generation]
*****

Repeat this structure for each significant scene in the book, making sure to include the string of 5 asterisks after each scene and ensuring that the breakdown captures the essence of the story and provides enough detail for creating illustrations.
Here is the text:
'''

    try:
        response = model.generate_content([prompt + story], safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        })
        
        if handle_safety_error(response):
            return []
        
        scenes = response.text.split(delimiter)
        print(scenes[0])
        return [scene.strip() for scene in scenes if scene.strip()]
    
    except Exception as e:
        print(f"Error in get_scenes: {e}")
        return []


def generate_images_and_audio_for_scenes(scenes):
    # with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        audio_tasks = []
        for i, scene in enumerate(scenes):
            print(f"Generating image and audio for scene {i+1}...")
            prompt = get_image_prompt(scene)
            audio_prompt = get_audio_prompt(scene)
            
            if audio_prompt:
                # audio_tasks.append(pool.apply_async(generate_audio, (audio_prompt, i)))
                print("Generating audio for scene", i+1)
                audio_tasks.append(musicgen.generate_music(audio_prompt, f'scene_{i+1}'))
                print("Audio generated for scene", i+1)
            
            if prompt:
                try:
                    create_image(prompt, f'scene_{i+1}', get_summary(scene))
                except:
                    print(f"Error generating image for scene {i+1}")
            else:
                print(f"Prompt not found for scene {i+1}")
        
        # Wait for all audio generation tasks to complete
        # for task in audio_tasks:
        #     result = task.get()
        #     print(result)
        

def story_to_images(story):
    scenes = get_scenes(story)
    generate_images_and_audio_for_scenes(scenes)
