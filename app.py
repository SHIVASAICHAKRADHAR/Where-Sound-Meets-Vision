import streamlit as st
import google.generativeai as genai
from PIL import Image
from langchain_google_genai import GoogleGenerativeAI
import os
from gtts import gTTS
import speech_recognition as sr  # Importing SpeechRecognition for voice input

st.balloons()
st.snow()

# title with white background
st.markdown("""
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #0044cc; /* Blue color */
            background-color: #f0f0f0; /* Light grey background */
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }
    </style>
    <div class="title">
        🌟 Empowering Vision: Chakradhar's AI-Driven Solution for Visually Impaired Assistance 🤖 📝
    </div>
""", unsafe_allow_html=True)

# Language options for TTS
language_options = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Hindi': 'hi',
    'Chinese': 'zh',
    'Japanese': 'ja',
    'Korean': 'ko',
}

# Sidebar for selecting language
selected_language = st.sidebar.selectbox("Choose Language for Text-to-Speech", list(language_options.keys()))

# Function to capture voice and convert it to text
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("🎤 Please speak...")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        st.write(f"Recognized text: {recognized_text}")
        return recognized_text
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        st.error("Could not request results from the speech recognition service.")
        return None

# Function to convert text to speech in selected language
def text_to_speech(text, lang='en'):
    """Converts the given text into speech in the specified language."""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_file = "output.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        st.error(f"Error in text-to-speech: {e}")
        return None

# Main Section: image upload, scene description, etc.
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    st.markdown("<h3 class='feature-header'> 🚂 Features </h3>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    # Box for Scene Description
    if col1.button("🖼️ **Illustrate Scene**", key="1", help="Describe the scene in detail and offer insights"):
        with st.spinner("Analyzing the scene..."):
            try:
                # Your existing logic for describing the scene goes here
                response = "Scene description here"  # Replace with your actual scene description
                text = f"Scene Description: {response}"

                # Convert the scene description to speech in selected language
                audio_file = text_to_speech(text, lang=language_options[selected_language])
                if audio_file:
                    with open(audio_file, "rb") as file:
                        st.audio(file.read(), format="audio/mp3")
                    os.remove(audio_file)
                st.write(response)
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Box for Voice Input (recognize speech from the user)
    if col2.button("🎙️ **Speak to Convert to Text**", key="2", help="Speak to convert your voice to text and hear the response"):
        recognized_text = recognize_speech_from_mic()
        if recognized_text:
            # Convert recognized speech to speech again (TTS)
            audio_file = text_to_speech(recognized_text, lang=language_options[selected_language])
            if audio_file:
                with open(audio_file, "rb") as file:
                    st.audio(file.read(), format="audio/mp3")
                os.remove(audio_file)

st.markdown(
    """
    <style>
        footer {
            background: linear-gradient(45deg, #ff6ec7, #ffc3a0, #ff9a8b, #ff6a00);
            padding: 20px;
            font-size: 24px;
            color: white;
            text-align: center;
            border-radius: 15px;
            animation: color-change 5s infinite alternate;
        }

        @keyframes color-change {
            0% {
                background: #ff6ec7;
            }
            25% {
                background: #ffc3a0;
            }
            50% {
                background: #ff9a8b;
            }
            75% {
                background: #ff6a00;
            }
            100% {
                background: #ff6ec7;
            }
        }
    </style>
    <footer>
        Made by <strong>Shiva Sai Chakradhar</strong> | Created for Accessibility | Built with 💝 for Visual Impaired 🧍🏻
    </footer>
    """,
    unsafe_allow_html=True,
)
