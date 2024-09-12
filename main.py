import streamlit as st
import openai
import speech_recognition as sr
from google.cloud import texttospeech
from io import BytesIO
import os

# Initialize OpenAI API
openai.api_key = 'your-openai-api-key'

# Initialize Google Cloud Text-to-Speech client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_google_credentials.json"
tts_client = texttospeech.TextToSpeechClient()

# Function to get chatbot response from OpenAI API
def get_chatbot_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Function to convert text to speech using Google Cloud
def text_to_speech(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="az-AZ",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    audio_file = BytesIO(response.audio_content)
    return audio_file

# Function to convert speech to text
def speech_to_text(audio_data):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_data) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='az')
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError:
        return "Could not request results"

# Streamlit application
st.title("Azerbaijani Voice Chatbot")

st.write("Record your voice question below:")

# Audio recording via Streamlit
audio_bytes = st.audio("record", format="audio/wav")

if audio_bytes:
    # Convert speech to text
    user_input = speech_to_text(BytesIO(audio_bytes))
    st.write(f"You said: {user_input}")
    
    if user_input:
        # Get chatbot response
        response_text = get_chatbot_response(user_input)
        st.write(f"Chatbot response: {response_text}")
        
        # Convert text response to speech
        audio_response = text_to_speech(response_text)
        st.audio(audio_response, format='audio/mp3')
