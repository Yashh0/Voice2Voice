import streamlit as st
import requests
import whisper
import azure.cognitiveservices.speech as speechsdk
from pathlib import Path

# Configure Streamlit page
st.set_page_config(page_title="Audio File Transcription", page_icon="🎤", layout="wide")

# Load Secrets
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    AZURE_SPEECH_KEY = st.secrets["AZURE_SPEECH_KEY"]
    AZURE_REGION = st.secrets["AZURE_REGION"]
except Exception as e:
    st.error("Missing secrets. Please configure required API keys in the app settings.")
    st.stop()


from pydub import AudioSegment

# Resample audio to 16kHz .wav format
def resample_audio(input_audio):
    try:
        audio = AudioSegment.from_file(input_audio)
        audio = audio.set_frame_rate(16000)  # Set sample rate to 16kHz
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio.export(temp_wav.name, format="wav")
        return temp_wav.name
    except Exception as e:
        st.error(f"Error resampling audio: {str(e)}")
        return None

# Initialize Whisper Model
@st.cache_resource
def load_model():
    with st.spinner("Loading Whisper model..."):
        return whisper.load_model("base")

whisper_model = load_model()

# Azure Text-to-Speech
def text_to_speech(text, subscription_key, region):
    try:
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        result = synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            st.audio(result.audio_data, format="audio/wav")
        else:
            st.error("Speech synthesis failed")
    except Exception as e:
        st.error(f"Azure TTS Error: {str(e)}")

# Groq AI Query
def query_groq(api_key, user_message):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 2000,
        "top_p": 0.9
    }
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Groq API Error: {str(e)}")
        return None

# File Upload and Processing
import tempfile
from pydub import AudioSegment

# File Upload and Processing
def process_audio_file(audio_file):
    try:
        with st.spinner("Processing audio file..."):
            # Resample audio to 16kHz .wav format
            temp_wav = resample_audio(audio_file)
            if temp_wav is None:
                st.error("Failed to resample audio file.")
                return

            # Transcribe audio
            st.subheader("🎤 Transcription")
            transcription_result = whisper_model.transcribe(temp_wav)  # Pass the resampled audio file
            transcription = transcription_result['text'].strip()
            st.write(transcription)

            # Get AI response
            st.subheader("🤖 AI Response")
            ai_response = query_groq(GROQ_API_KEY, transcription)
            if ai_response:
                st.write(ai_response)

                # Option to convert AI response to speech
                if st.checkbox("Convert AI response to speech"):
                    text_to_speech(ai_response, AZURE_SPEECH_KEY, AZURE_REGION)
    except Exception as e:
        st.error(f"Error processing audio file: {str(e)}")


# Streamlit UI
st.title("🎤 Audio File Transcription & AI Assistant")
st.write("Upload an audio file to transcribe and get AI assistance.")

# Upload Button
uploaded_file = st.file_uploader("Choose an audio file (supported formats: .wav, .mp3, .m4a)", type=["wav", "mp3", "m4a"])

# Process the file
if uploaded_file:
    process_audio_file(uploaded_file)
