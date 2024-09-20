from story_processor import *
from inputter import *

input_file_name = 'datafiles/short_story.pdf'
if input_file_name.endswith('.pdf'):
    inp = Inputter(input_source=input_file_name, flag=1)
elif input_file_name.endswith('.docx'):
    inp = Inputter(input_source=input_file_name, flag=2)
elif input_file_name.endswith('.txt'):
    inp = Inputter(input_source=input_file_name, flag=3)
else:
    raise ValueError("Invalid file format")

inp = Inputter(input_source=input_file_name, flag=1)

cleanedtext = inp.clean_text(inp.read_pdf())
print(cleanedtext)
story_to_images(cleanedtext)