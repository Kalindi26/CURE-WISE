import os
import platform
from gtts import gTTS
from playsound import playsound
from dotenv import load_dotenv



def text_to_speech_with_gtts(text, output_file="doctor_response_gtts.mp3"):
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(output_file)
    print(f"[gTTS] Saved to {output_file}")
    try:
        playsound(output_file)
    except Exception as e:
        print(f"[gTTS] Playback error: {e}")




if __name__ == "__main__":
    input_text = "Hello, this is your AI doctor. How can I assist you today?"

    
    text_to_speech_with_gtts(input_text, "doctor_response_gtts.mp3")

    



