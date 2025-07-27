import os
import time
import shutil
import gradio as gr
from dotenv import load_dotenv

from voice_of_patient import transcribe_with_groq
from voice_of_doctor import text_to_speech_with_gtts
from brain_of_doctor import encode_image, analyze_image_with_query, analyze_text_only

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Ensure folders exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("responses", exist_ok=True)

system_prompt = (
    "You have to act as a professional doctor, i know you are not but this is for learning purpose. "
    "What's in this image?. Do you find anything wrong with it medically? "
    "If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in "
    "your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person. "
    "Donot say 'In the image I see' but say 'With what I see, I think you have ....' "
    "Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, "
    "Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"
)

def process_inputs(audio_filepath, image_filepath):
    if not GROQ_API_KEY:
        return "Missing GROQ API Key", "", None

    # Save audio input
    timestamp = int(time.time())
    if audio_filepath:
        audio_upload_path = os.path.join("uploads", f"user_audio_{timestamp}.wav")
        shutil.copy(audio_filepath, audio_upload_path)

    # Transcribe
    try:
        transcription = transcribe_with_groq("whisper-large-v3", audio_filepath, GROQ_API_KEY)
    except Exception as e:
        return f"Transcription failed: {e}", "", None

    query = system_prompt + "\n" + transcription

    # Save transcription
    with open(os.path.join("uploads", f"user_transcript_{timestamp}.txt"), "w", encoding="utf-8") as f:
        f.write(transcription)

    # Analyze
    if image_filepath:
        try:
            # Save image input
            image_upload_path = os.path.join("uploads", f"user_image_{timestamp}.jpg")
            shutil.copy(image_filepath, image_upload_path)

            encoded = encode_image(image_filepath)
            model = "meta-llama/llama-4-scout-17b-16e-instruct"
            response = analyze_image_with_query(query, model, encoded)
        except Exception as e:
            response = f"Image analysis failed: {e}"
    else:
        try:
            model = "groq/llama3-8b-8192"
            response = analyze_text_only(query, model)
        except Exception as e:
            response = f"Text analysis failed: {e}"

    # Save doctor response
    with open(os.path.join("responses", f"doctor_text_response_{timestamp}.txt"), "w", encoding="utf-8") as f:
        f.write(response)

    # Generate speech
    try:
        audio_path = os.path.join("responses", f"doctor_voice_{timestamp}.mp3")
        text_to_speech_with_gtts(response, audio_path)
    except Exception as e:
        audio_path = None
        response += f" (Voice generation failed: {e})"

    return transcription, response, audio_path


# --- Gradio UI ---
with gr.Blocks(gr.themes.Soft(primary_hue="sky", secondary_hue="gray")) as iface:

    gr.Markdown("""
    # 🩺🧠⚕️ CURE WISE -Healing meets intelligence."
    Talk to the AI doctor and optionally upload an image of your skin issue. This assistant listens, analyzes, and responds to your concerns.
    """)

    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="🎤 Speak your symptoms")
        image_input = gr.Image(type="filepath", label="🖼️ Upload image (optional)")

    submit_btn = gr.Button("🩺 Submit to AI Doctor")

    with gr.Row():
        text_output = gr.Textbox(label="📝 Transcribed Speech")
        diagnosis_output = gr.Textbox(label="🧠 Doctor's Response")

    audio_output = gr.Audio(label="🔊 Doctor's Voice")

    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[text_output, diagnosis_output, audio_output]
    )

iface.launch(debug=True)

