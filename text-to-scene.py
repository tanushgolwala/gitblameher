
import os
import dotenv

dotenv.load_dotenv()
API_KEY = os.getenv('GEMINI_KEY')

import google.generativeai as genai
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

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
*****

Repeat this structure for each significant scene in the book,making sure to include the string of 5 asterisks after each scene and ensuring that the breakdown captures the essence of the story and provides enough detail for creating illustrations.
Here is the text:
'''

story = '''Once upon a time, three little pigs decided to leave home and build their own houses. The first pig, a bit lazy, built his house out of straw because it was the quickest and easiest to construct. The second pig, a little more cautious, built his house from sticks, thinking it would be stronger but still manageable. The third pig, the most diligent, worked hard to build his house out of bricks, making it sturdy and strong.

One day, a big bad wolf came along, hungry and determined to eat the pigs. He went to the first pig's house and said, “Little pig, little pig, let me come in!” The pig refused, so the wolf huffed and puffed and blew the straw house down easily. The first pig ran to his brother’s house.

The wolf then went to the second pig’s house made of sticks. Again, he demanded to come in, and when the pigs refused, the wolf huffed and puffed and blew the stick house down. The two pigs ran to their third brother’s house.

Finally, the wolf came to the third pig’s house made of bricks. He huffed and puffed, but no matter how hard he tried, the brick house stood strong. Frustrated, the wolf decided to try sneaking down the chimney, but the clever third pig had a pot of boiling water waiting. When the wolf came down, he fell into the pot, got burned, and ran away, never to bother the pigs again.

The three little pigs lived safely in the sturdy brick house, happy and content.
'''

response = model.generate_content(prompt + story)
delimiter="*****"
scenes = response.text.split(delimiter)
print(scenes[0])

