import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
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


if st.button("🪄 Fix Sentence", type="primary"):
    if current_text:
        with st.spinner("AI is thinking..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash', 
                    contents=f"Turn these ASL letters into a sentence: {current_text}"
                )
                
                st.success(f"**AI Translation:** {response.text}")
            except Exception as e:
                st.error(f"AI Error: {e}")