import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("GEMINI_API_KEY")

# Configure generative model
genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name='gemini-1.5-flash')

# Generate content
response = model.generate_content("give me a book of story")
print(response.text)
