# 🩺 CURE WISE – Healing Meets Intelligence

**CURE WISE** is an AI-powered virtual doctor built using Gradio, Groq (for transcription and image understanding), and gTTS (for voice responses). It allows users to **speak their symptoms**, optionally upload a **medical image**, and receive **spoken medical advice** — all in a visually soothing interface.

---

## 🌟 Features

- 🎤 **Voice Input**: Speak your symptoms into the microphone.
- 🖼️ **Image Upload**: Optionally upload skin or medical images for diagnosis.
- 💬 **Doctor’s Response**: Get a concise, doctor-like answer in natural language.
- 🔊 **Audio Reply**: Hear your diagnosis using realistic text-to-speech.
- 🎨 **Lavender-themed UI**: A beautiful and calm design for better experience.

---

## Screen Shots

<img src="<img width="1879" height="890" alt="Screenshot 2025-09-05 135832" src="https://github.com/user-attachments/assets/a4a0104f-5485-4c98-a63b-e01d5f61c278" />
" alt="CURE WISE UI" width="600"/>

## 📁 Project Structure

```bash
├── app.py                 # Gradio app entry point
├── voice_of_patient.py    # Audio recording + transcription with Groq
├── voice_of_doctor.py     # Text-to-speech (gTTS + ElevenLabs optional)
├── brain_of_doctor.py     # Image and text analysis via Groq LLM
├── requirements.txt       # All necessary Python libraries
├── uploads/               # User-uploaded audio/images (auto-created)
├── responses/             # Audio response files (auto-created)
└── .env                   # Environment variables (not pushed to GitHub)
⚙️ Installation
1. Clone the Repo

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Create & Activate Virtual Environment

python -m venv venv
venv\Scripts\activate    # Windows
# OR
source venv/bin/activate # macOS/Linux

3. Install Dependencies
pip install -r requirements.txt

4. Add Environment Variables
Create a .env file in the root folder with the following content:
GROQ_API_KEY=your_groq_api_key_here
ELEVEN_API_KEY=your_elevenlabs_api_key_here  # optional

🚀 Run the App

python app.py

🧠 Models Used
Groq Whisper – Transcribes voice to text.

Groq LLaMA Vision – Analyzes medical images with language prompts.


