import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import re
from config import load_config
import os
from comicators.comicator import face_text_adder
from imagegen import create_image,  create_image_cloudflare
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

def get_dialogue(scene_info):
    match = re.search(r'\*\*Dialogue:\*\*(.*)', scene_info)
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
    prompt = '''Given a text-based story, break it down into distinct scenes suitable for a comic book adaptation. For each scene:

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
10. Provide one dialogue for each scene by the main character in that scene. The dialogue should be a short sentence that captures the essence of the scene.

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
Dialogue: [Short sentence by the main character in the scene]
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
        
        print(response)
        
        if handle_safety_error(response):
            return []
        
        scenes = response.text.split(delimiter)
        print(scenes[0])
        return [scene.strip() for scene in scenes if scene.strip()]
    
    except Exception as e:
        print(f"Error in get_scenes: {e}")
        return []


def generate_images_and_audio_for_scenes(scenes):
    audio_tasks = []
    for i, scene in enumerate(scenes):
        print(f"Processing scene {i+1}...")
        prompt = get_image_prompt(scene)
        # audio_prompt = get_audio_prompt(scene)
        dialogue = get_dialogue(scene)
        
        # if audio_prompt:
        #     print(f"Generating audio for scene {i+1}")
        #     audio_tasks.append(musicgen.generate_music(audio_prompt, f'scene_{i+1}'))
        #     print(f"Audio generated for scene {i+1}")
        
        if prompt:
            try:
                initial_image_path = f'scene_{i+1}'
                create_image_cloudflare(prompt, initial_image_path, get_summary(scene))
                print(initial_image_path)
                
                if not os.path.exists(f"image_outputs/{initial_image_path}.png"):
                    print(f"image_outputs/{initial_image_path}.png")
                    raise FileNotFoundError(f"Image file {initial_image_path} was not created")
                
                if dialogue:
                    output_image_path = f'scene_{i+1}_with_dialogue.png'
                    try:
                        face_text_adder(f"image_outputs/{initial_image_path}.png", f"dialogue_outputs/{output_image_path}", dialogue)
                        print(f"Added dialogue to image for scene {i+1}")
                    except Exception as e:
                        print(f"Error adding dialogue to image for scene {i+1}: {str(e)}")
                        print("Skipping dialogue addition and using the original image.")
                        output_image_path = initial_image_path
                else:
                    print(f"No dialogue found for scene {i+1}")
                    output_image_path = initial_image_path
                
                print(f"Final image for scene {i+1} saved as: {output_image_path}")
            
            except FileNotFoundError as e:
                print(f"Error: {str(e)}")
                print("Image generation failed. Skipping this scene.")
            except Exception as e:
                print(f"Unexpected error processing scene {i+1}: {str(e)}")
                print("Skipping this scene.")
        else:
            print(f"Prompt not found for scene {i+1}")        
        # Wait for all audio generation tasks to complete
        # for task in audio_tasks:
        #     result = task.get()
        #     print(result)
        

def story_to_images(story):
    scenes = get_scenes(story)
    generate_images_and_audio_for_scenes(scenes)


story = '''
**Cinderella's Longer Story**

Once upon a time, in a faraway kingdom, there lived a kind-hearted girl named Cinderella. She was the daughter of a wealthy man who remarried after her mother’s passing. Her father’s new wife, however, was a cruel and selfish woman. She brought along her two daughters, who were just as unkind. After Cinderella’s father passed away, her stepmother and stepsisters treated her like a servant. While they wore fine clothes and enjoyed their days, Cinderella was made to do all the housework, cook meals, and sleep in a dusty attic.

Despite her harsh life, Cinderella remained gentle and hopeful, often finding comfort in the small animals around her who became her friends. She longed for a better life, but she never complained or became bitter.

One day, a royal messenger arrived with exciting news: the king was hosting a grand ball for his son, the prince, and all the eligible young women in the kingdom were invited. The ball was intended to help the prince find a bride. Cinderella was thrilled and asked her stepmother if she could attend. But her stepmother, jealous of Cinderella’s beauty, cruelly said she could only go if she finished all her chores and found something suitable to wear. Cinderella worked hard to finish everything, but when she asked again, her stepmother and stepsisters laughed at her and ripped apart the only dress she had, leaving her in tears as they went off to the ball without her.

As Cinderella wept in the garden, her Fairy Godmother appeared. She waved her wand and, in an instant, transformed a pumpkin into a magnificent carriage, mice into horses, and Cinderella’s rags into a beautiful gown of shimmering fabric. On her feet appeared delicate glass slippers. “You shall go to the ball,” said the Fairy Godmother, “but remember, the magic will wear off at midnight.”

Cinderella arrived at the palace, where everyone, including her stepmother and stepsisters, was amazed by the mysterious and beautiful girl. Even the prince was captivated. He danced with Cinderella all night, and they talked and laughed together, forgetting the world around them. As the clock neared midnight, Cinderella remembered the Fairy Godmother’s warning. Without explanation, she fled the palace, running so quickly that she lost one of her glass slippers on the staircase. She disappeared just as the clock struck twelve, and her dress turned back into rags. 

The next day, the prince, determined to find the girl he had fallen in love with, declared that he would search the kingdom to find the one whose foot fit the glass slipper. He and his guards traveled from house to house, trying the slipper on every young woman. When they arrived at Cinderella’s home, her stepsisters eagerly tried to force their feet into the slipper, but it didn’t fit. Just as they were about to leave, Cinderella stepped forward and asked to try. Her stepmother and stepsisters scoffed, but the prince’s men let her try on the slipper. To everyone’s surprise, it fit perfectly! 

In that moment, the Fairy Godmother’s magic revealed Cinderella’s true identity, and the prince knew she was the girl from the ball. Overjoyed, he asked her to marry him. Cinderella, now free from her cruel family, accepted, and they were married in a grand celebration. From that day on, Cinderella lived happily in the palace, her kindness and grace recognized by all. And she never forgot the lessons of humility, hope, and love that had guided her through her darkest days.

And so, Cinderella and the prince lived happily ever after.
'''
story_to_images(story=story)
