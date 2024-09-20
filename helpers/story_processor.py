import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import re
from config import load_config
from imagegen import create_image

def initialize_model():
    config = load_config()
    genai.configure(api_key=config['api_key'])
    return genai.GenerativeModel(config['model_name'])

def get_image_prompt(scene_info):
    match = re.search(r'\*\*Prompt:\*\*(.*)', scene_info)
    return match.group(1).strip() if match else None

def get_summary(scene_info):
    match = re.search(r'\*\*Summary:\*\*(.*?)\*\*Characters:', scene_info, re.DOTALL)
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
7. Suggest a vivid visual element that could represent the scene in a picture.
8. Using the above details provide a prompt that could be used to generate an image using an AI model, that depicts every part of the image

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


def generate_images_for_scenes(scenes):
    for i,scene in enumerate(scenes):
        prompt = get_image_prompt(scene)
        if prompt:
            try:
                create_image(prompt,f'scene_{i+1}',get_summary(scene))
            except:
                print(f"Error generating image for scene {i+1}")
        else:
            print(f"Prompt not found for scene {i+1}")
        

def story_to_images(story):
    scenes = get_scenes(story)
    generate_images_for_scenes(scenes)


story = '''Once upon a time, in a small Italian village, there lived an old woodcarver named Geppetto. He was a kind man, but lonely, and spent his days crafting wooden toys. One day, with great care, he carved a puppet that looked like a little boy. He named it Pinocchio.

That night, as Geppetto slept, a magical blue fairy visited his workshop. She waved her wand over the puppet, bringing Pinocchio to life. She whispered, "Be kind, brave, and honest, and one day, you will become a real boy."

The next morning, Geppetto was astonished to find Pinocchio walking and talking. Overjoyed, he treated Pinocchio like a son. However, Pinocchio was mischievous and curious, often finding himself in trouble. He didn’t always tell the truth, and every time he lied, his nose would grow longer.

One day, Pinocchio met a sly fox and a cunning cat who tricked him into leaving school and following them. They led him into a world of trouble, where he was nearly sold as a performer in a puppet show. Escaping with the help of the blue fairy, Pinocchio promised to be good but struggled to keep his word.

His adventures took him to strange places, even to the bottom of the ocean where he was swallowed by a giant whale. Inside the whale, Pinocchio found Geppetto, who had been searching for him. Pinocchio bravely rescued Geppetto, and they made their way back home.

Through his bravery and love for Geppetto, Pinocchio learned the value of honesty and kindness. The blue fairy, seeing his change of heart, granted his wish, and Pinocchio became a real boy. Geppetto and Pinocchio lived happily ever after, knowing that truth and love made their bond stronger than ever.
'''

story_to_images(story)