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
    youtube_url = st.text_input("Enter the YouTube video URL")

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
            
# import streamlit as st
# import openai
# import whisper
# import os
# import yt_dlp
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain.chains import RetrievalQA

# # Ensure OpenAI API key is set
# openai.api_key = os.getenv("OPENAI_API_KEY")
# if not openai.api_key:
#     st.error("OpenAI API key is not set. Please set it in your environment variables or .env file.")
#     st.stop()

# def load_model():
#     # Load Whisper model with fallback to CPU if GPU is unavailable
#     try:
#         st.write("Loading Whisper model...")
#         return whisper.load_model("base", device="cpu")
#     except Exception as e:
#         st.error(f"Error loading Whisper model: {e}")
#         return None

# def extract_audio_from_youtube(youtube_url):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'quiet': True,
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }]
#     }
#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(youtube_url, download=False)
#             return info_dict.get('url', None)
#     except Exception as e:
#         st.error(f"Error extracting audio from YouTube: {e}")
#         return None

# def transcribe_youtube_audio(youtube_url):
#     model = load_model()
#     if not model:
#         return "Failed to load Whisper model."
    
#     audio_url = extract_audio_from_youtube(youtube_url)
#     if not audio_url:
#         return "Failed to extract audio from YouTube."
    
#     try:
#         result = model.transcribe(audio_url)
#         return result["text"]
#     except Exception as e:
#         st.error(f"Error transcribing audio: {e}")
#         return "Failed to transcribe audio."

# def get_recipe_response(user_query, retriever):
#     try:
#         # Ensure OpenAI's ChatCompletion is properly initialized
#         qa_chain = RetrievalQA.from_chain_type(llm=openai.ChatCompletion.create, retriever=retriever)
#         return qa_chain.run(user_query)
#     except Exception as e:
#         st.error(f"Error generating recipe response: {e}")
#         return "Failed to generate recipe response."

# # Streamlit UI
# st.title("🍳 AI Recipe & Cooking Assistant")

# # Input for YouTube video URL
# youtube_url = st.text_input("Enter YouTube video URL")
# retriever = None

# # Initialize retriever with error handling
# try:
#     retriever = Chroma(embedding_function=OpenAIEmbeddings()).as_retriever()
# except Exception as e:
#     st.error(f"Error initializing retriever: {e}")

# if youtube_url:
#     st.video(youtube_url)
#     transcribed_text = transcribe_youtube_audio(youtube_url)
#     st.write("### Transcribed Recipe Instructions:", transcribed_text)

# # Input for user query
# user_query = st.text_input("Ask a cooking question (e.g., How to knead dough?)")
# if user_query and retriever:
#     response = get_recipe_response(user_query, retriever)
#     st.write("### AI Response:", response)

# # AI Image Caption Generator
# st.title("AI ingredients Identifier ")
# uploaded_image = st.file_uploader("Upload an image to identify ingredients", type=["png", "jpg", "jpeg"])

# if uploaded_image:
#     image = Image.open(uploaded_image)
#     st.image(image, caption="Uploaded Image")

#     if st.button("Identify Ingredients"):
#         try:
#             with st.spinner("Identify ingredients..."):
#                 response = client.models.generate_content(
#                     model="gemini-2.0-flash",
#                     contents=["List down only those ingredients that you can identify with 90 percent accuracy in this image ?"],
#                     config=types.GenerateContentConfig(
#                         response_modalities=['Text']
#                     )
#                 )
#                 st.subheader("Identified ingredients:")
#                 st.write(response.candidates[0].content.parts[0].text)
#         except Exception as e:
#             st.error(f"Error Identify ingredients: {e}")