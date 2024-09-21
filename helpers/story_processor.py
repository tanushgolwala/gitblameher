import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import re
from config import load_config
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
                    audio_tasks.append(musicgen.generate_music(audio_prompt, f'scene_{i+1}'))
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


story = '''
### The Three-Headed Dog
It starts when Harry, Ron, Hermione, and Neville are out of bed after hours and trying to avoid being caught by Filch, the caretaker. They flee through dark corridors, their footsteps echoing against the cold stone, until they reach a door. In their panic, they slip inside without checking where it leads. 

Inside, they come face-to-face with Fluffy, the enormous three-headed dog. Its gigantic paws shuffle across the floor, each head snapping and snarling with teeth bared. The creature is clearly guarding something. While Harry’s heart pounds, he notices that Fluffy stands on a trapdoor. The significance of this doesn’t escape him, and as the trio hurriedly retreats from the room, it dawns on them that whatever Fluffy is guarding must be of great importance—likely the Philosopher's Stone itself.

### Discovering the Plot
From this moment on, Harry, Ron, and Hermione can't shake the idea that someone is trying to steal the stone. They suspect Professor Snape, whose strange behavior throughout the school year—especially after Harry’s broom was jinxed during a Quidditch match—makes him the obvious culprit in their eyes. The three friends decide they need to stop whoever is trying to get to the stone.

The trio investigates further, and through a series of clues, they learn that the stone, created by Nicolas Flamel, grants immortality and is hidden behind a series of magical defenses. With no time to lose, they resolve to descend through the trapdoor and protect the stone themselves.

### Entering the Trapdoor
On the night of their plan, they sneak through the castle once more, covered by Harry's invisibility cloak. Reaching the door guarded by Fluffy, they discover Hagrid’s unintentional tip: Fluffy can be lulled to sleep with music. Using a small harp, they charm the beast, and it soon collapses into a heavy slumber. Carefully, they slip through the trapdoor, lowering themselves into the unknown below.

### Devil's Snare
Their descent takes them into a dark, eerie room filled with writhing, snake-like vines—the Devil’s Snare. As soon as they land, the vines tighten around them like deadly ropes. Hermione remembers that Devil's Snare hates light and heat, so she conjures a bright blue flame, causing the plant to recoil and release them. They breathe a sigh of relief, but know that this is only the beginning.

### The Winged Keys
The next challenge awaits in a vast chamber filled with fluttering, enchanted keys. A broomstick hovers nearby, and they quickly realize that the key to the next door is hidden among the chaotic swarm. Harry mounts the broomstick, his Seeker instincts kicking in, as he darts through the air, weaving through the mass of glittering wings. After a tense chase, he manages to grab the correct key, and they hurry to the next room.

### The Chessboard
Here, they encounter a life-sized enchanted chessboard. To move forward, they must play through the game. Ron, a skilled chess player, takes charge, directing their moves from atop the giant pieces. The match is grueling, and the chess pieces battle fiercely. With every move, Ron calculates the best strategy to win, even if it means sacrifice. Near the end, Ron sees that the only way for Harry and Hermione to advance is if he allows himself to be taken. In a bold and selfless move, Ron positions himself where the opposing queen strikes him down, leaving him unconscious. Harry and Hermione move forward with heavy hearts, knowing Ron’s sacrifice could be in vain if they fail.

### The Potions Riddle
The next room is filled with black flames blocking their path and purple flames guarding the entrance behind them. In the middle stands a table with several potions. It’s a test of logic, and Hermione takes the lead, reading the riddle carefully. After a tense moment of thought, she identifies the correct potions, and Harry drinks one that will allow him to pass through the black flames. Hermione, meanwhile, stays behind, ready to help Ron and summon help if needed.

### The Final Confrontation: Quirrell
Harry enters the final chamber, expecting to face Snape—but instead, it’s Professor Quirrell who stands before the Mirror of Erised. The timid professor, once thought to be afraid of his own shadow, is revealed as the true villain. It is Quirrell who has been trying to steal the stone all along, under the influence of someone far more sinister: Lord Voldemort.

Harry is frozen in shock as Quirrell explains that Voldemort has been sharing his body. The Dark Lord, too weak to survive on his own, has been hiding within Quirrell, biding his time. Quirrell orders Harry to look into the Mirror of Erised, which shows one’s deepest desire. As Harry gazes into the mirror, he sees his reflection holding the Philosopher’s Stone—and to his surprise, he feels the stone drop into his pocket. He doesn’t reveal this to Quirrell, trying to play for time.

But Voldemort, sensing Harry’s deception, commands Quirrell to seize the boy. In the ensuing struggle, Harry’s touch causes Quirrell immense pain. His skin blisters and burns wherever Harry grabs him. Voldemort, desperate, urges Quirrell to kill Harry, but Quirrell crumbles under Harry’s touch. With every second, Quirrell weakens, and Voldemort, in a final act of desperation, abandons his host’s body and flees as a wraith, leaving Harry to collapse, unconscious.

### Dumbledore's Arrival and Aftermath
When Harry awakens, he’s in the hospital wing, with Dumbledore sitting at his side. The headmaster explains that the stone has been destroyed, and with it, any chance of Voldemort returning to full power for now. Dumbledore also reveals that Harry’s mother, Lily, left a powerful protection on him when she sacrificed her life, which is why Quirrell couldn’t touch him.

Harry learns that Ron and Hermione are safe, and they share a moment of quiet relief, knowing they prevented a great disaster. However, Harry also understands that Voldemort is not gone for good—only driven away, waiting for another chance to rise.

### The House Cup
As the school year draws to a close, Harry, Ron, and Hermione return to normal life at Hogwarts, but not without one last surprise. During the House Cup feast, Dumbledore awards points to Gryffindor for the bravery, intelligence, and friendship they displayed during their adventure. With these points, Gryffindor wins the House Cup, much to the shock and delight of the entire house.

The trio’s first year at Hogwarts ends with victory, but also with the knowledge that greater challenges lie ahead.
'''
story_to_images(story=story)
