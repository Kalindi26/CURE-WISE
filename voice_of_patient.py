import os
import logging
import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
STT_MODEL = "whisper-large-v3"

def record_audio(filename="patient_voice.wav", duration=5, fs=44100):
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

if __name__ == "__main__":
    output_file = "patient_voice.wav"
    record_audio(filename=output_file, duration=8)

    if os.path.exists(output_file):
        result = transcribe_with_groq(output_file, STT_MODEL, GROQ_API_KEY)
        if result:
            print("\n🗣️ Transcribed Text:", result)
        else:
            print("❌ Failed to transcribe.")
    else:
        print("❌ Audio file not found.")
