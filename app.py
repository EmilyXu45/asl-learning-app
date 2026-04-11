import streamlit as st
# create the frontend of the app/
import cv2
# Allows us to use the camera and process the images
from PIL import Image
# Pillow: resize/format the picture inputs 
import numpy as np
# Process the images as numbers and feed them into the model
import base64
# Turn image into text that can be sent to the backend
import random
from openai import OpenAI
import google.generativeai as genai

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=st.secrets["FEATHERLESS_API_KEY"])

# Initialize 'page' in session state if it doesn't exist.
if 'page' not in st.session_state:
    st.session_state.page = "home"

def asl_fact():
    try:
        fact = client.chat.completions.create(
            model="Magistral-Small-2507-Rebased-Vision",
            messages= [{"role": "user", "content": "Tell me one short, inspiring, or interesting random fact about ASL or the Deaf community. Keep it under 30 words."}],
            max_tokens=60
        )
        return fact.choices[0].message.content.strip()
    except:
        return "There are over 300 different sign languages used around the world? ASL is just one of them!"

if st.session_state.page == "home":
    st.title("Let's Learn ASL!")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🤟 Practice Lab", use_container_width=True):
            st.session_state.page = "app" 
            st.rerun()

    with col2:
        if st.button("🤖 Beat the Robot", use_container_width=True):
            st.switch_page("pages/quiz.py")
    
    with col3:
        if st.button("✍️ Sentence Maker", width="stretch"):
            st.switch_page("pages/sentence_maker.py")

    #SDG Cards Display Section:

    st.divider()
    st.subheader("🌍 UN Sustainable Development Goals")
    st.write("Hover over the cards to see how this app contributes!")

    #Two columes to display the 2 SDG cards side by sider
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="flip-card">
              <div class="flip-card-inner">
                <div class="flip-card-front">
                  <img src="https://raw.githubusercontent.com/EmilyXu45/asl-learning-app/d0a068fa355aa14763dec78c45a7fb79d3a25d7a/images/sdg4.png" style="width:100%"; height:auto;>
                </div>
                <div class="flip-card-back">
                  <p><b>Making sign language learning accessible to everyone through AI-powered interactive tools.</b></p>
                </div>
              </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="flip-card">
              <div class="flip-card-inner">
                <div class="flip-card-front">
                 <img src="https://raw.githubusercontent.com/EmilyXu45/asl-learning-app/d0a068fa355aa14763dec78c45a7fb79d3a25d7a/images/sdg10.png" style="width:100%"; height:auto;>
                </div>
                <div class="flip-card-back">
                  <p><b>Breaking communication barriers to ensure deaf and hard-of-hearing individuals have equal opportunities.</b></p>
                </div>
              </div>
            </div>
        """, unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("💡 Did you know?")
        if st.button("Generate New Fact"):
            st.session_state.asl_fact = asl_fact()
            
        if 'asl_fact' not in st.session_state:
            st.session_state.asl_fact = asl_fact()
        st.write(st.session_state.asl_fact)
    
    
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    local_css("style.css")
   

elif st.session_state.page == "app":
    if st.button("⬅️ Home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("""
    ### How it works:
    1. **Get a Letter:** The AI will challenge you with a random letter.
    2. **Strike a Pose:** Show your hand sign to the camera.
    3. **Get Instant Feedback:** Our Vision AI will tell you if you're correct or how to improve!
    """
    )

    if 'target' not in st.session_state:
        st.session_state['target'] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    # Initialize the target letter in the session state if it doesn't exist
    # Prevent the target letter from resetting on every interaction (every 1 sec)
    st.header(f"Can you sign the letter {st.session_state['target']}?")

    if st.button("Give me a different letter"):
        st.session_state.target = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        st.rerun()
    st.info("💡 Tip: Make sure your hand is well-lit and clearly visible in the frame!")

    img_file_buffer = st.camera_input("Take a photo of your sign:")
    # Opens the camera and takes a picture which gets stored in img_file_buffer
    if img_file_buffer is not None:
        img = Image.open(img_file_buffer)
        with st.spinner("Checking your sign..."):
                try:
                    prompt = f"The user is trying to sign the ASL letter '{st.session_state.target}'. Is it correct? Explain why or why not briefly."
                    
                    response = model.generate_content([prompt, img])
                    result = response.text
                    
                    st.info(f"Feedback: {result}")
                    
                    if "correct" in result.lower() and "not" not in result.lower():
                        st.balloons()
                        st.success("Perfect!")
                    else:
                        st.warning("Keep trying!")
                        
                except Exception as e:
                    st.error(f"Error: {e}")