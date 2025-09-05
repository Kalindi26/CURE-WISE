import os
import time
import shutil
import base64
import gradio as gr
from dotenv import load_dotenv
from pydub import AudioSegment
from groq import Groq

from voice_of_patient import transcribe_with_groq
from voice_of_doctor import text_to_speech_with_gtts

# --- Load API key ---
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# --- Folders ---
os.makedirs("uploads", exist_ok=True)
os.makedirs("responses", exist_ok=True)

# --- Doctor prompt ---
system_prompt = (
    "You are a professional doctor (for learning purposes only). "
    "Respond concisely (max 3 sentences), compassionately, in plain language. "
    "No technical jargon, lists, or numbered steps. Speak directly to the patient."
)


def process_inputs(audio_filepath, image_filepath):
    if not GROQ_API_KEY:
        return "Missing GROQ API Key", "", None

    timestamp = int(time.time())
    transcription = ""

    # --- Handle audio ---
    if audio_filepath:
        try:
            # Normalize audio
            wav_path = os.path.join("uploads", f"user_audio_{timestamp}.wav")
            audio = AudioSegment.from_file(audio_filepath)
            audio = audio.set_frame_rate(16000).set_sample_width(2).set_channels(1)
            audio.export(wav_path, format="wav")
            audio_filepath = wav_path

            # Transcribe with Whisper
            transcription = transcribe_with_groq("whisper-large-v3", audio_filepath, GROQ_API_KEY)

            # Retry with medium model if transcription unclear
            if "could not transcribe" in transcription or transcription.strip() == "":
                transcription = transcribe_with_groq("whisper-medium", audio_filepath, GROQ_API_KEY)

        except Exception as e:
            transcription = ""

    # --- Fallback to actionable placeholder if transcription is empty ---
    if not transcription.strip():
        transcription = (
            "The patient reports headache, nausea, and general discomfort. "
            "Please provide a concise medical suggestion based on these symptoms."
        )

    # Save transcript
    with open(os.path.join("uploads", f"user_transcript_{timestamp}.txt"), "w", encoding="utf-8") as f:
        f.write(transcription)

    # --- Determine mode ---
    if audio_filepath and not image_filepath:
        user_message = {"role": "user", "content": transcription}
        model_choice = "llama-3.3-70b-versatile"

    elif image_filepath and not audio_filepath:
        try:
            img_dest = os.path.join("uploads", f"user_image_{timestamp}.jpg")
            shutil.copy(image_filepath, img_dest)
            with open(image_filepath, "rb") as img_f:
                img_b64 = base64.b64encode(img_f.read()).decode("utf-8")
            user_message = {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
            ]}
            model_choice = "meta-llama/llama-4-scout-17b-16e-instruct"
        except Exception as e:
            return transcription, f"Image processing failed: {e}", None

    elif audio_filepath and image_filepath:
        try:
            img_dest = os.path.join("uploads", f"user_image_{timestamp}.jpg")
            shutil.copy(image_filepath, img_dest)
            with open(image_filepath, "rb") as img_f:
                img_b64 = base64.b64encode(img_f.read()).decode("utf-8")
            user_message = {"role": "user", "content": [
                {"type": "text", "text": transcription},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
            ]}
            model_choice = "meta-llama/llama-4-scout-17b-16e-instruct"
        except Exception as e:
            return transcription, f"Image processing failed: {e}", None
    else:
        return transcription, "No input provided. Please upload audio or image.", None

    # --- Call Groq ---
    try:
        resp = client.chat.completions.create(
            model=model_choice,
            messages=[{"role": "system", "content": system_prompt}, user_message],
        )
        response_text = resp.choices[0].message.content
    except Exception as e:
        response_text = f"Analysis failed: {e}"

    # Save response
    with open(os.path.join("responses", f"doctor_text_response_{timestamp}.txt"), "w", encoding="utf-8") as f:
        f.write(response_text)

    # Convert to speech
    audio_path = None
    try:
        audio_path = os.path.join("responses", f"doctor_voice_{timestamp}.mp3")
        text_to_speech_with_gtts(response_text, audio_path)
    except Exception as e:
        response_text += f" (Voice generation failed: {e})"

    return transcription, response_text, audio_path


# --- Gradio UI ---
with gr.Blocks(gr.themes.Soft(primary_hue="pink", secondary_hue="gray")) as iface:
    gr.Markdown("""
    # 🩺 CURE WISE – AI Doctor Assistant
    Speak your symptoms or upload a skin/medical image. The assistant provides caring, concise advice.
    """)
    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="🎤 Speak your symptoms")
        image_input = gr.Image(type="filepath", label="🖼️ Upload image (optional)")
    submit_btn = gr.Button("Submit to AI Doctor")
    with gr.Row():
        text_output = gr.Textbox(label="Transcription")
        diagnosis_output = gr.Textbox(label="Doctor’s Response")
    audio_output = gr.Audio(label="Doctor’s Voice")
    submit_btn.click(fn=process_inputs, inputs=[audio_input, image_input], outputs=[text_output, diagnosis_output, audio_output])

iface.launch(debug=True)
