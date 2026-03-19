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

Client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=st.secrets["FEATHERLESS_API_KEY"])

st.title("ASL Learning App")
st.write("Testing the camera...")

img_file_buffer = st.camera_input("Take a photo of a sign:")
# Opens the camera and takes a picture which gets stored in img_file_buffer
if img_file_buffer is not None:
# Checking if the user has taken a picture to be processsed.
    img = Image.open(img_file_buffer)
    st.image(img, caption="Sign visible", use_container_width = True)
    st.success("Camera is working, WOOHOO!")