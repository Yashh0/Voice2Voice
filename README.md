# Voice2Voice



# Audio File Transcription & AI Assistant

This project allows users to upload an audio file, transcribe the audio using OpenAI's Whisper model, and get AI assistance based on the transcription. Additionally, the AI response can be converted to speech using Azure's Text-to-Speech service.

# Access the Model
[Voice2Voive](https://huggingface.co/spaces/yash001010/Voice2Voice)

## Features

- Upload audio files (supported formats: `.wav`, `.mp3`, `.m4a`)
- Transcribe audio to text using Whisper model
- Query AI using the transcription with Groq's AI model
- Optionally convert AI responses to speech using Azure Text-to-Speech
- Streamlit-based user interface

## Requirements
```
streamlit==1.31.0
numpy==1.24.3
requests==2.31.0
sounddevice==0.4.6
soundfile==0.12.1
ffmpeg-python==0.2.0
openai-whisper==20231117
azure-cognitiveservices-speech==1.31.0
torch==2.1.0
torchaudio==2.1.0
python-dotenv==1.0.0

```

### Python Version

- Python 3.8 or higher

### Dependencies

You need to install the following Python packages to run the application:

```bash
pip install streamlit whisper requests azure-cognitiveservices-speech pydub
```
# Additional Setup
Azure Speech API:

# Set up an Azure Cognitive Services account.
Obtain the AZURE_SPEECH_KEY and AZURE_REGION from your Azure portal.
Groq API:

Set up an account with Groq.
Obtain the GROQ_API_KEY to query Groq's AI models.
Streamlit Secrets:

Store the API keys in your secrets.toml file (Streamlit's secret management).
toml
Copy code
```
[GROQ_API_KEY]
key = "your-groq-api-key"

[AZURE_SPEECH_KEY]
key = "your-azure-speech-key"

[AZURE_REGION]
region = "your-azure-region"
How to Run the App
Run the Streamlit app:

```
Open your terminal and navigate to the project directory. Then, run:

bash
Copy code
```
streamlit run app.py
```
Upload an Audio File:

Open the app in your browser (default URL: http://localhost:8501).
Upload an audio file in .wav, .mp3, or .m4a format.
View Transcription and AI Response:

The app will transcribe the audio file and display the text.
You will then see the AI-generated response based on the transcription.
Convert AI Response to Speech (Optional):

You can convert the AI response into speech using Azure's Text-to-Speech service by checking the box provided in the UI.
Project Structure
bash
Copy code
```
.
├── app.py                # Main Streamlit app file
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── secrets.toml          # Streamlit secrets for API keys

```
This project is licensed under the MIT License - see the LICENSE file for details.

