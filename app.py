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

st.title("ASL Learning App")

client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=st.secrets["FEATHERLESS_API_KEY"])

if 'target' not in st.session_state:
    st.session_state['target'] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
# Initialize the target letter in the session state if it doesn't exist
# Prevent the target letter from resetting on every interaction (every 1 sec)
st.header(f"Can you sign the letter {st.session_state['target']}?")

if st.button("Give me a different letter"):
    st.session_state.target = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    st.rerun()

st.write("Show your sign to the camera!")

img_file_buffer = st.camera_input("Take a photo of your sign:")
# Opens the camera and takes a picture which gets stored in img_file_buffer
if img_file_buffer is not None:
# Checking if the user has taken a picture to be processsed.
    img = Image.open(img_file_buffer)
    st.image(img, caption="Sign visible", use_container_width = True)
    st.success("Camera is working, WOOHOO!")

# 1. Convert the camera image to Base64 text for the AI
    bytes_data = img_file_buffer.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')

    # 2. Ask the AI to grade the sign
    with st.spinner("Checking your sign..."):
        try:
            response = client.chat.completions.create(
                model="pixtral-12b",
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
            
            if "correct" in result.lower():
                st.balloons()
                
        except Exception as e:
            st.error(f"Uh-oh, something went wrong. Error: {e}")
        # Exception handling