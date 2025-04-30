import streamlit as st
import google.generativeai as genai
from PIL import Image
from langchain_google_genai import GoogleGenerativeAI
import os
from gtts import gTTS
import speech_recognition as sr

# Initialize Google Generative AI model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key="AIzaSyBXMcdtCJ2OQtAOaBpztTAjQjJnjmBLIWg")

# Custom function to convert text to speech in different languages
def text_to_speech(text, language='en'):
    """Function to convert text to speech in the specified language."""
    # Remove any colons from the text
    cleaned_text = text.replace(":", "")
    
    # Convert the cleaned text to speech in the chosen language
    audio_file = "output_1.mp3"
    tts = gTTS(text=cleaned_text, lang=language, slow=False)
    tts.save(audio_file)
    
    return audio_file

# Function for speech recognition to choose language
def recognize_language():
    """Recognize user's spoken language choice (Hindi or Telugu)."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.write("🎤 Please speak 'Hindi' or 'Telugu' to choose your preferred language.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            # Recognize the speech and return language choice
            speech = recognizer.recognize_google(audio).lower()
            st.write(f"Detected speech: {speech}")
            if "telugu" in speech:
                return 'te'
            elif "hindi" in speech:
                return 'hi'
            else:
                st.write("Couldn't detect 'Telugu' or 'Hindi'. Defaulting to English.")
                return 'en'  # Default language is English
        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand the speech. Please try again.")
            return 'en'
        except sr.RequestError:
            st.write("Sorry, there was an issue with the speech recognition service.")
            return 'en'

# UI for selecting language
language_option = st.radio(
    "Select a language for voice output:",
    ("English", "Hindi", "Telugu"),
    index=0
)

# Text-to-speech in selected language
if language_option == "Hindi":
    lang_code = "hi"
elif language_option == "Telugu":
    lang_code = "te"
else:
    lang_code = "en"

# File upload section
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Call the language-specific Text-to-Speech function after a button is pressed
    if st.button("Describe Scene"):
        with st.spinner("Analyzing the scene..."):
            try:
                # Your existing code to get the scene description
                response = "This is a test description of the uploaded image."
                audio_file = text_to_speech(response, language=lang_code)

                # Play the audio response
                with open(audio_file, "rb") as file:
                    st.audio(file.read(), format="audio/mp3")
                os.remove(audio_file)
                st.write(response)
            except Exception as e:
                st.error(f"Error: {str(e)}")
