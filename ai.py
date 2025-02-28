import requests # type: ignore
import json
import os
import dotenv # type: ignore

dotenv.load_dotenv()

def ai_recommendations(prompt):
    key = os.getenv("OPENAI_API_KEY")
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer " + key,
    },
    data=json.dumps({
        "model": "cognitivecomputations/dolphin3.0-r1-mistral-24b:free", # Optional
        "messages": [
        {
            "role": "user",
            "content": prompt
        }
        ]
    })
    )
    content = response.json()['choices'][0]['message']['content']
    if len(content)>0 and "error" not in content:
        return {
            "status_code": 200,
            "content": content,
        }
    else:
        return {
            "status_code": 500,
            "content": "Sorry, I couldn't understand that. Please try again.",
        }
