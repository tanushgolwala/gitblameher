
import os
import dotenv
from imagegen import create_image
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

dotenv.load_dotenv()
API_KEY = os.getenv('GEMINI_KEY')

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


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

Repeat this structure for each significant scene in the book,making sure to include the string of 5 asterisks after each scene and ensuring that the breakdown captures the essence of the story and provides enough detail for creating illustrations.
Here is the text:
'''

    response = model.generate_content([prompt + story],safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    print(response)
    scenes = response.text.split(delimiter)
    return scenes


import re

def get_image_prompt(sceneInfo):
    # print(sceneInfo)
    match = re.search(r'\*\*Prompt:\*\*(.*)', sceneInfo)
    if match:
        return match.group(1).strip()
    return None

story = '''
Julius Caesar: A Story of Ambition and Betrayal

Julius Caesar was born in 100 BCE into a patrician family in Rome. His early life was marked by political turmoil, as the Roman Republic faced power struggles between various factions, particularly the populares (who sought reform for the common people) and the optimates (the traditionalist elite). From a young age, Caesar showed ambition and a talent for oratory, which would serve him well in his political career.

Rise to Power

Caesar began his political career as a military officer. He served in Asia and Cilicia and quickly earned a reputation for bravery and leadership. In 60 BCE, he formed the First Triumvirate, an informal alliance with two powerful figures: Pompey, a celebrated general, and Crassus, the wealthiest man in Rome. This alliance helped him secure the position of consul in 59 BCE, but it also created tensions with the Senate, which was wary of his growing influence.

After his consulship, Caesar was appointed governor of Gaul. From 58 to 50 BCE, he led a series of military campaigns known as the Gallic Wars, successfully conquering the region and expanding Roman territory. His military prowess and the wealth he brought to Rome increased his popularity among the Roman people, but it also deepened the animosity between him and the Senate, particularly with Pompey, who had become increasingly concerned about Caesar's power.

Crossing the Rubicon

In 49 BCE, tensions reached a breaking point. The Senate, influenced by Pompey, ordered Caesar to disband his army and return to Rome. Rather than comply, Caesar famously crossed the Rubicon River, declaring, "The die is cast." This act of defiance ignited a civil war between Caesar's supporters and those loyal to Pompey. After a series of battles, Caesar emerged victorious, culminating in the defeat of Pompey at the Battle of Pharsalus in 48 BCE. Pompey fled to Egypt, where he was assassinated.

Dictatorship and Reforms

Upon returning to Rome, Caesar was appointed dictator. He initiated a series of reforms aimed at addressing various social and economic issues. He redistributed land to veterans, reformed the calendar (creating the Julian calendar), and expanded the Senate to include more representatives from the provinces. His popularity soared among the common people, but his concentration of power alarmed the Senate and many aristocrats.

Caesar declared himself "dictator for life" in 44 BCE, a title that evoked memories of kingship—something Romans were deeply opposed to. His reforms, while popular, further alienated the Senate, who feared he would undermine the Republic.

The Ides of March

On March 15, 44 BCE—the Ides of March—Caesar attended a Senate meeting despite warnings from a soothsayer to "beware the Ides of March." A group of conspirators, including notable senators like Brutus and Cassius, plotted his assassination. They believed that by killing him, they could restore the Republic and prevent him from becoming a tyrant.

As Caesar entered the Senate, he was surrounded by the conspirators. Brutus, whom he regarded as a friend, delivered the final blow. The senators stabbed him multiple times, with Caesar famously uttering "Et tu, Brute?" ("And you, Brutus?") as he fell. His assassination shocked Rome and led to chaos.

Legacy

Caesar’s death did not restore the Republic; instead, it plunged Rome into further civil wars. His adopted heir, Octavian (later Augustus), ultimately emerged as the victor. The events following Caesar's assassination led to the end of the Roman Republic and the establishment of the Roman Empire.

Caesar’s legacy endures in history as a brilliant military leader and a controversial figure whose ambition reshaped Rome. His life and death have inspired countless works of art, literature, and political thought, cementing his place as one of history's most significant figures.
'''

scenes = get_scenes(story)
for i in range(len(scenes)):
    create_image(get_image_prompt(scenes[i]), "scene" + str(i) + ".png")