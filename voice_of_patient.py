from dotenv import load_dotenv
import os
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import logging
from groq import Groq

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# GROQ API key and model
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
stt_model = "whisper-large-v3"
output_file = "patient_voice.wav"  # WAV format, no ffmpeg needed

def record_audio(filename=output_file, duration=5, fs=44100):
    try:
        logging.info("Recording started. Speak now...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        write(filename, fs, recording)
        logging.info(f"Recording saved as {filename}")
    except Exception as e:
        logging.error(f"Error during recording: {e}")

def transcribe_with_groq(audio_file_path, model, api_key):
    try:
        client = Groq(api_key=api_key)
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                language="en"
            )
        return transcription.text
    except Exception as e:
        logging.error(f"Transcription error: {e}")
        return ""

# Run the pipeline
record_audio(duration=8)  # You can increase duration as needed
if os.path.exists(output_file):
    result = transcribe_with_groq(output_file, stt_model, GROQ_API_KEY)
    if result:
        print("\n🗣️ Transcribed Text:", result)
    else:
        print("❌ Failed to transcribe.")
else:
    print("❌ Audio file not found.")
