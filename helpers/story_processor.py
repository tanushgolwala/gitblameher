import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import re
from helpers.config import load_config
from helpers.imagegen import create_image,  create_image_cloudflare
import helpers.musicgen

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

# def generate_audio(audio_prompt, scene_index):
#     return generate_music(audio_prompt, f'scene_{scene_index+1}')

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
        print(response.text)
        scenes = response.text.split(delimiter)
        return [scene.strip() for scene in scenes if scene.strip()]
    
    except Exception as e:
        print(f"Error in get_scenes: {e}")
        return []


def generate_images_and_audio_for_scenes(scenes):
    # with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        audio_tasks = []
        for i in range(len(scenes)):
            try:
                scene = scenes[i]
                print(f"Generating image and audio for scene {i+1}...")
                prompt = get_image_prompt(scene)
                audio_prompt = get_audio_prompt(scene)
                
                print("Generating image for scene", i+1)
                if prompt:
                    try:
                        create_image_cloudflare(prompt, f'scene_{i+1}', get_summary(scene))
                    except:
                        print(f"Error generating image for scene {i+1}")
                else:
                    print(f"Prompt not found for scene {i+1}")

                print("Generating audio for scene", i+1)
                if audio_prompt:
                    # audio_tasks.append(pool.apply_async(generate_audio, (audio_prompt, i)))
                    print("Generating audio for scene", i+1)
                    audio_tasks.append(helpers.musicgen.generate_music(audio_prompt, f'audio_outputs/scene_{i+1}.wav',600))
                    print("Audio generated for scene", i+1)
                
            except Exception as e:
                print(f"Error in generate_images_and_audio_for_scenes: {e}. Retrying scene {i+1}...")
                i = i - 1
                continue
        
        # Wait for all audio generation tasks to complete
        # for task in audio_tasks:
        #     result = task.get()
        #     print(result)
        

def story_to_images(story):
    scenes = get_scenes(story)
    generate_images_and_audio_for_scenes(scenes)
    return len(scenes)


if __name__ == "__main__":
    story = '''
    Julius Caesar’s life is filled with remarkable events that significantly influenced Roman history. Here’s a deeper look into his story:

    ### Early Life and Rise to Power
    Caesar was born into the patrician class, a noble lineage, but his family wasn’t particularly wealthy or powerful at the time. He married into powerful political circles, and his early career was marked by political maneuvers, including an alliance with Crassus, Rome’s wealthiest man, and Pompey, Rome’s greatest general. This alliance, known as the **First Triumvirate** (60 BCE), helped him secure the position of consul in 59 BCE.

    ### The Gallic Wars and Military Genius
    After his consulship, Caesar was appointed governor of several Roman provinces, including Gaul. From 58 to 50 BCE, he led the **Gallic Wars**, expanding Roman territory and subjugating various tribes across modern-day France, Belgium, and parts of Germany. Caesar’s victories were both brutal and brilliant, showcasing his military strategy and leadership. His conquest of Gaul brought immense wealth and prestige, making him one of the most powerful men in Rome.

    During this period, he also wrote his famous work, *Commentarii de Bello Gallico* (Commentaries on the Gallic War), detailing his campaigns and solidifying his image as a skilled general.

    ### Conflict with Pompey and the Civil War
    As Caesar’s power grew, tensions with Pompey and the Senate escalated. Pompey, once Caesar’s ally, became his adversary, aligning with the Senate to curb Caesar’s influence. In 49 BCE, the Senate ordered Caesar to disband his army and return to Rome as a private citizen. Refusing, Caesar made the momentous decision to **cross the Rubicon River** with his army, famously saying, “The die is cast.” This act of defiance was treason and initiated a civil war.

    Caesar swiftly marched on Rome, forcing Pompey and his supporters to flee to Greece. After pursuing and defeating Pompey’s forces in a series of battles, most notably at the **Battle of Pharsalus** (48 BCE), Caesar emerged victorious. Pompey fled to Egypt, where he was assassinated. Caesar then became embroiled in Egyptian politics, supporting Cleopatra’s claim to the throne. Their famous relationship resulted in the birth of a son, **Caesarian**.

    ### Dictatorship and Reforms
    Returning to Rome, Caesar was appointed **dictator** in 49 BCE, initially for a short term, but in 44 BCE he was declared **dictator for life**. During his rule, Caesar enacted numerous reforms aimed at strengthening Rome. He restructured the debt system, reformed the calendar (introducing the **Julian calendar**, a precursor to the modern Gregorian calendar), and expanded the Senate to include representatives from across the Roman territories.

    Caesar also granted citizenship to people in the provinces and began extensive building projects, reshaping the city of Rome. His reforms, however, increasingly alienated the Roman elite, particularly the Senate, who feared he was becoming a monarch.

    ### The Ides of March and Caesar’s Assassination
    Despite his popularity among the common people, many senators saw Caesar as a threat to the Republic. A group of 60 senators, including his close friend **Brutus** and **Cassius**, conspired to assassinate him. On **March 15, 44 BCE**, the Ides of March, Caesar was attacked in the Senate chamber. He was stabbed 23 times, and according to legend, his last words were “**Et tu, Brute?**” (You too, Brutus?), expressing his shock at Brutus’s betrayal.

    ### Aftermath and Legacy
    Caesar’s assassination plunged Rome into further civil wars. His adopted heir and grandnephew, **Octavian** (later Augustus), along with Mark Antony, sought revenge on the conspirators, ultimately defeating them in the **Battle of Philippi**. This paved the way for the eventual rise of the Roman Empire, with Octavian becoming its first emperor.

    Caesar’s legacy is profound:
    - He ended the Roman Republic and laid the foundation for the Roman Empire.
    - His military campaigns, particularly in Gaul, extended Roman influence and set the standard for future generals.
    - His reforms, particularly the Julian calendar, had lasting impacts.
    - The title “Caesar” became synonymous with leadership, later used by emperors and influencing titles like “Kaiser” in Germany and “Tsar” in Russia.

    Julius Caesar’s life is a testament to ambition, military genius, and political power, but also a reminder of how unchecked ambition can lead to betrayal and downfall.
    '''
    story_to_images(story=story)
