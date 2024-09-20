import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import re
from config import load_config

def initialize_model():
    config = load_config()
    genai.configure(api_key=config['api_key'])
    return genai.GenerativeModel(config['model_name'])

def get_image_prompt(scene_info):
    match = re.search(r'\*\*Prompt:\*\*(.*)', scene_info)
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

def get_scenes(story, delimiter="*****"):
    model = initialize_model()
    prompt = '''Given a text-based story, break it down into distinct scenes suitable for a picture book adaptation. For each scene:

1. Identify the key action or event that defines the scene.
2. Provide a brief summary of what happens in the scene (2-3 sentences).
3. List the characters present in the scene.
4. Describe the setting, including:
   - Location
   - Time of day (if relevant)
   - Any important environmental details (weather, atmosphere, etc.)
5. Note any significant objects or props that play a role in the scene.
6. Highlight any emotional tone or mood that's important to convey.
7. Suggest a vivid visual element that could represent the scene in a picture.
8. Using the above details provide a prompt that could be used to generate an image using an AI model, that depicts every part of the image

Format the output as follows:

Scene [Number]: [Key Action/Event]
Summary: [Brief description of what happens]
Characters: [List of characters present]
Setting:
- Location: [Where the scene takes place]
- Time: [Time of day, if relevant]
- Details: [Important environmental elements]
Objects: [List of significant objects or props]
Tone: [Emotional tone or mood of the scene]
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
        return [scene.strip() for scene in scenes if scene.strip()]
    
    except Exception as e:
        print(f"Error in get_scenes: {e}")
        return []
