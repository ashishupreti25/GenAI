import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the API key is set
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY is not set. Please set it in your .env file.")
    st.stop()

# Initialize the GenAI client
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"Error initializing GenAI client: {e}")
    st.stop()

# Add custom CSS for the "Quicksand" font
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.title("🍳 AI Cooking Companion")

# Sidebar menu with clickable labels
st.sidebar.header("Menu")
if st.sidebar.button("YouTube Cooking Assistant"):
    st.session_state.menu_option = "YouTube Cooking Assistant"
if st.sidebar.button("Image-Based Recipe Suggestions"):
    st.session_state.menu_option = "Image-Based Recipe Suggestions"

menu_option = st.session_state.get("menu_option", None)

if menu_option == "YouTube Cooking Assistant":
    # AI YouTube Video Summarizer
    st.title("Youtube Cooking Assitant")
    youtube_url = st.text_input("Enter the YouTube cooking video URL")

    #Display the video if a URL is provided
    if youtube_url:
        st.video(youtube_url)


    if st.button("Generate Instructions"):
        if not youtube_url:
            st.warning("Please enter the YouTube video URL")
        else:
            try:
                with st.spinner("Generating Instructions..."):
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=types.Content(
                            parts=[
                                types.Part(text="List down the cooking instructions and ingredients list with alternate options?"),
                                types.Part(
                                    file_data=types.FileData(file_uri=youtube_url)
                                )
                            ]
                        )
                    )
                    st.subheader("Instructions Summary:")
                    st.write(response.candidates[0].content.parts[0].text)
            except Exception as e:
                st.error(f"Error generating video instructions: {e}")

elif menu_option == "Image-Based Recipe Suggestions":
    st.title("Image-Based Recipe Suggestions")
    uploaded_image = st.file_uploader("Upload an image to identify ingredients", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image")

        if st.button("Get Ingredients & Recipe Suggestions"):
            try:
                with st.spinner("Identifing Ingredients..."):
                    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=["list down the ingredients that you can identify in this image also mention the dish or dishes that can be made using these ingredients?", image])
                    st.subheader("Ingredients identified:")
                    st.write(response.text)
            except Exception as e:
                st.error("Error Identifing Ingredients")
            
