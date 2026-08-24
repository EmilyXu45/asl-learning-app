import streamlit as st
import random
from PIL import Image
from google import genai
from navigation import render_sidebar

# 1. Render shared sidebar
render_sidebar()

# 2. Apply styling
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("style.css")

# 3. Initialize Gemini Client
gemini_client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# 4. Page UI
st.title("🤟 ASL Practice Lab")

st.markdown("""
### How it works:
1. **Get a Letter:** The AI will challenge you with a random letter.
2. **Strike a Pose:** Show your hand sign to the camera.
3. **Get Instant Feedback:** Our Vision AI will tell you if you're correct or how to improve!
""")

# Initialize target letter in session state
if 'target' not in st.session_state:
    st.session_state['target'] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

st.header(f"Can you sign the letter {st.session_state['target']}?")

if st.button("Give me a different letter"):
    st.session_state.target = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    st.rerun()

st.info("💡 Tip: Make sure your hand is well-lit and clearly visible in the frame!")

# Camera Input
img_file_buffer = st.camera_input("Take a photo of your sign:")

if img_file_buffer is not None:
    img = Image.open(img_file_buffer)
    st.image(img, caption="Your Sign", use_container_width=True)

    with st.spinner("AI is checking your sign..."):
        try:
            response = gemini_client.models.generate_content(
                model='gemini-2.0-flash', 
                contents=[
                    f"The user is trying to sign the ASL letter '{st.session_state.target}'. Is it correct? Explain briefly.",
                    img
                ]
            )
            
            result = response.text
            st.info(f"Feedback: {result}")
            
            if "correct" in result.lower() and "not" not in result.lower():
                st.balloons()
                st.success("Perfect! You got it!")
            else:
                st.warning("Not quite there yet, try again!")

        except Exception as e:
            st.error(f"AI Error: {e}. Tip: Check your GOOGLE_API_KEY in Secrets.")