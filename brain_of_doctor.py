from dotenv import load_dotenv
import os
import base64
from groq import Groq

# Load environment variables
load_dotenv()

# Step 1: Setup API Key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise Exception("GROQ_API_KEY not set in environment.")

# Step 2: Encode image

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Step 3a: Analyze image + text

def analyze_image_with_query(query, model, encoded_image):
    client = Groq(api_key=GROQ_API_KEY)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
            ],
        }
    ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )
    return chat_completion.choices[0].message.content

# Step 3b: Analyze text only

def analyze_text_only(query, model):
    client = Groq(api_key=GROQ_API_KEY)
    messages = [
        {"role": "user", "content": query}
    ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )
    return chat_completion.choices[0].message.content

# Step 4: Run test manually
# Step 4: Run test manually
if __name__ == "__main__":
    image_path = "acne.jpg"
    query = "Is there something wrong with my face?"
    model = "meta-llama/llama-4-scout-17b-16e-instruct"  # ✅ Supported model for vision
    encoded = encode_image(image_path)
    response = analyze_image_with_query(query, model, encoded)
    print("Response received:")
    print(response)

