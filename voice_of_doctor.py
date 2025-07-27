import os
import platform
from gtts import gTTS
from playsound import playsound
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

# --------------- gTTS SECTION ------------------

def text_to_speech_with_gtts(text, output_file="doctor_response_gtts.mp3"):
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(output_file)
    print(f"[gTTS] Saved to {output_file}")
    try:
        playsound(output_file)
    except Exception as e:
        print(f"[gTTS] Playback error: {e}")

# --------------- ElevenLabs SECTION ------------------

from elevenlabs import save, play, VoiceSettings
from elevenlabs.client import ElevenLabs

def text_to_speech_with_elevenlabs(text, output_file="doctor_response_eleven.mp3"):
    if not ELEVEN_API_KEY:
        raise ValueError("Missing ELEVEN_API_KEY in environment variables.")

    client = ElevenLabs(api_key=ELEVEN_API_KEY)
    audio = client.generate(
        text=text,
        voice="Aria",  # You can replace this with another voice name
        model="eleven_turbo_v2",
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75)
    )
    save(audio, output_file)
    print(f"[ElevenLabs] Saved to {output_file}")
    try:
        play(output_file)
    except Exception as e:
        print(f"[ElevenLabs] Playback error: {e}")

# ------------------ USAGE ----------------------

if __name__ == "__main__":
    input_text = "Hello, this is your AI doctor. How can I assist you today?"

    # Option 1: Use gTTS
    text_to_speech_with_gtts(input_text, "doctor_response_gtts.mp3")

    # Option 2: Use ElevenLabs (uncomment to use)
    # text_to_speech_with_elevenlabs(input_text, "doctor_response_eleven.mp3")




