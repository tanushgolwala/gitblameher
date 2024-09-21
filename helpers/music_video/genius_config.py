import os
import dotenv

def load_config():
    dotenv.load_dotenv()
    return {
        'api_key': os.getenv('GEMINI_KEY'),
        'model_name': "gemini-1.5-flash",
        'scene_delimiter': "*****"
    }
