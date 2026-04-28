
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import requests

load_dotenv()

def generate(catagories,title,site):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash"
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"do you think this site contains one or more of these catagories:{', '.join(catagories)}? answer in yes or no only! this is its title: {title} and this is its html script: {site} "),
            ],
        ),
    ]

    tools = [
        types.Tool(google_search=types.GoogleSearch()),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(include_thoughts=False),
        max_output_tokens=500,
    )
    

    try:
        answer= " "
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            for part in chunk.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text:
                    answer += part.text
        return answer.strip()                
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    r=requests.get("https://.com")
    generate([],"",r.text)
