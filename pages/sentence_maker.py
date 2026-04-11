import streamlit as st
from openai import OpenAI
import google.generativeai as genai

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("✍️ ASL Sentence Maker")

if st.button("⬅️ Home"):
    st.session_state.page = "home"
    st.switch_page("app.py")

if 'draft_letters' not in st.session_state:
    st.session_state.draft_letters = []


col_main, col_keys = st.columns([2, 1])

with col_keys:
    st.write("### ⌨️ ASL Keyboard")
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ " 
    # Create a 4-column grid for buttons
    k_cols = st.columns(4)
    for i, char in enumerate(alphabet):
        label = "Space" if char == " " else char
        if k_cols[i % 4].button(label, key=f"k_{char}", width="stretch"):
            st.session_state.draft_letters.append(char)
            st.rerun()

with col_main:
    st.write("### Your Draft")
    current_text = "".join(st.session_state.draft_letters)
    
    st.info(f"👉 **{current_text}**" if current_text else "Click letters to start...")
    
    if st.button("Clear All 🗑️", width="stretch"):
        st.session_state.draft_letters = []
        st.rerun()

    st.divider()


    if st.button("🪄 Fix with AI", type="primary", width="stretch"):
        if not current_text:
            st.warning("Type some letters first!")
        else:
            with st.spinner("Gemini is thinking..."):
                try:
                    prompt = f"Turn these ASL letters into a correct English sentence: {current_text}. Fix typos, add spaces and punctuation. Return ONLY the sentence."
                    
                    response = model.generate_content(prompt)
                    
                    st.success(f"**AI Translation:** {response.text}")
                except Exception as e:
                    st.error(f"AI Error: {e}")