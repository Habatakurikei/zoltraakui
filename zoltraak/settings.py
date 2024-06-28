import os
from dotenv import load_dotenv
from os.path import dirname
from os.path import join

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')

load_dotenv(dotenv_path)

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
