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

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🤟 Practice Lab", use_container_width=True):
            st.session_state.page = "app" 
            st.rerun()

    with col2:
        if st.button("🤖 Beat the Robot", use_container_width=True):
            st.switch_page("pages/quiz.py")
    
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
    if st.button("⬅️ Back to Home"):
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
    # Checking if the user has taken a picture to be processsed.
        img = Image.open(img_file_buffer)
        img_resized = img.resize((200,200), Image.Resampling.LANCZOS)
        import io
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=50)
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        st.image(img, caption="Sign visible", use_container_width = True)
        st.success("Checking may be slow, please be patient...")

    # 1. Convert the camera image to Base64 text for AI processing
        bytes_data = img_file_buffer.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')

        # 2. Ask the AI to grade the sign
        with st.spinner("Checking your sign..."):
            try:
                # Initiate chat completion with the vision model, sending the image and asking for feedback on the sign.
                response = client.chat.completions.create(
                    model="kmouratidis/Magistral-Small-2507-Rebased-Vision",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"The user is trying to sign the ASL letter '{st.session_state.target}'. Is it correct? If not, what letter are they actually making?"},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ],
                        }
                    ],
                )
                # Using vision model to analyse the image and determine if the sign is correct or not, and provide feedback.
                # Connecting to and asking the AI model to grade the sign and provide feedback.
                
                # 3. Show the result
                result = response.choices[0].message.content
                # Displaying the first AI message choice to the user
                st.info(f"Feedback: {result}")
                # Visually showing feedback
                
                if "is correct" in result.lower() and "not" not in result.lower():
                # Ensuring that "not" is absent to avoid false positives such as "not correct" where the word "correct" is present but the sign is incorrect.
                    st.balloons()
                    st.success("Perfect! You got it!")
                else:
                    st.warning("Not quite there yet, check the feedback and try again!")

            except Exception as e:
                st.error(f"Uh-oh, something went wrong. Error: {e}")
            # Exception handling
